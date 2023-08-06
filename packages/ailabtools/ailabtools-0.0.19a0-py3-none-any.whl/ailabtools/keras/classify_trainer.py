import os, sys
from datetime import datetime
import keras
from keras.callbacks import ModelCheckpoint, LearningRateScheduler
from keras.applications import mobilenet_v2

from ailabtools.keras.callbacks import TrainValTensorBoard
from ailabtools.keras.pairgenerator import PairDataGenerator
import ailabtools.statistic as st

def preprocess_image(x):
    x = x.astype(np.float32)
    x /= 127.5
    x -= 1.
    return x

def build_callbacks(model_name, base_log='.', base_lr=0.001):

    nowww = datetime.now()
    train_name = '{}_{}'.format(model_name, nowww.strftime("%Y-%m-%d_%H:%M:%S"))

    def check(path):
        if not os.path.exists(path):
            os.makedirs(path)
            
    base_log = os.path.join(base_log, train_name)
    log_dir = base_log+'/logs'
    train_dir = base_log+'/trains'
    
    check(base_log)
    check(log_dir)
    check(train_dir)

    def scheduler(epoch):
        drop_step = 5
        return base_lr*(0.9**(int(epoch/drop_step)))

    callbacks = [TrainValTensorBoard(log_dir=log_dir), 
                 ModelCheckpoint(train_dir
                                 +'/weights.{epoch:02d}-loss-{loss:.5f}-vloss-{val_loss:.5f}.hdf5', 
                                 monitor='val_loss', 
                                 verbose=1, 
                                 save_best_only=False),
                LearningRateScheduler(scheduler, verbose=1)]
    
    return callbacks

def train_classifier(train_set, 
    model=None, 
    num_class=2,
    pre_channel=128,
    last_softmax=True,
    input_shape=(224,224,3),
    val_set=None, 
    model_name='classifier', 
    checkpoint_path='./log', 
    base_lr=0.01, 
    optimizer='sgd', 
    metrics=['accuracy'], 
    loss='categorical_crossentropy', 
    epoch=10, 
    batch_size=16,
    auto_construct_weight=True,
    num_worker=4
):
    train_x, train_y = train_set

    # construct model
    print('constructing model...')
    input = keras.layers.Input(input_shape)
    if model == None:
        print('\tNo specified model, using MobilenetV2 1.0 as default')
        backbone = mobilenet_v2.MobileNetV2(input_shape=input_shape, alpha=1.0, include_top=False, pooling=None)
        backbone_x = backbone(input)
        x = keras.layers.GlobalMaxPooling2D()(backbone_x)
        if pre_channel > 0:
            x = keras.layers.Dense(pre_channel, activation='relu', name='pre', kernel_initializer='he_normal')(x)
        x = keras.layers.Dense(num_class, activation='sigmoid', name='logits', kernel_initializer='he_normal')(x)
        if last_softmax:
            x = keras.layers.Softmax(name='output')(x)
        model = keras.models.Model(input, x, name=model_name)
    model.summary()
    print('constructing model... DONE')

    print('Compiling model...')
    print('\tOptimizer: {}'.format(optimizer))
    print('\tLoss: {}'.format(loss))
    print('\tMetrics: {}'.format(metrics))
    model.compile(optimizer, loss=loss, metrics=metrics)
    print('Compiling model... DONE')

    weights_dict_int = None
    if auto_construct_weight:
        print('Constructing class weights...')
        weights_dict = st.get_weight_dict(train_x, train_y, multiply=3)
        weights_dict_int = {}
        for k in weights_dict:
            weights_dict_int[int(k)] = weights_dict[k]
            print('\tClass {}: {}'.format(k, weights_dict[k]))
        print('Constructing class weights... DONE')

    print('Constructing generator...')
    gen = PairDataGenerator(width_shift_range=0.1, 
                        height_shift_range=0.1, 
                        brightness_range=[0.7, 1.3], 
                        shear_range=0.0, 
                        zoom_range=[0.8, 1.2], 
                        channel_shift_range=0.2, 
                        horizontal_flip=True, 
                        vertical_flip=True,
                        preprocessing_function=preprocess_image)
    gen_val = None
    if val_set is not None:
        gen_val = PairDataGenerator(preprocessing_function=preprocess_image)
    print('Constructing generator... DONE')

    print('Constructing callbacks...')
    if not os.path.exists(checkpoint_path):
        os.makedirs(checkpoint_path)
    callbacks = build_callbacks(model_name, 
                        base_lr=base_lr, 
                        base_log=checkpoint_path)
    print('\tTo visualize training graph:')
    print('\t\ttensorboard --logdir={}'.format(checkpoint_path))
    print('Constructing callbacks... DONE')

    print('Start training process...')
    val_iter = None
    val_step = 0
    if val_set is not None:
        val_x, val_y = val_set
        val_iter = gen_val.flow_from_pair(val_x, val_y, batch_size=batch_size, target_size=input_shape[:2])
        val_step = len(val_x)//batch_size+1

    model.fit_generator(gen.flow_from_pair(train_x, train_y, batch_size=batch_size, target_size=input_shape[:2]),
                    validation_data=val_iter,
                    epochs=epoch,
                    steps_per_epoch=len(train_x)//batch_size+1,
                    validation_steps=val_step,
                    class_weight=weights_dict_int, 
                    workers=num_worker, 
                    callbacks=callbacks,
                    use_multiprocessing=True)
    print('Start training process... DONE')

    return model

