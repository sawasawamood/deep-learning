 # -*- coding: Shift-JIS -*-
import glob
import numpy as np

from keras.preprocessing.image import load_img, img_to_array, array_to_img
from keras.preprocessing.image import random_rotation, random_shift, random_zoom
from keras.layers.convolutional import Conv2D
from keras.layers.pooling import MaxPooling2D
from keras.layers.core import Activation
from keras.layers.core import Dense
from keras.layers.core import Dropout
from keras.layers.core import Flatten
from keras.models import Sequential
from keras.models import model_from_json
from keras.callbacks import LearningRateScheduler
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.utils import np_utils

FileNames = ["img1.npy", "img2.npy", "img3.npy"]
ClassNames = ["normal", "abnormal", "abnormal2"]
hw = {"height":32, "width":32}        # ���X�g�ł͂Ȃ������^ ���������ň͂�


################################
###### �摜�f�[�^�̑O���� ######
################################
def PreProcess(dirname, filename, var_amount=3):
    num = 0
    arrlist = []
    files = glob.glob(dirname + "/*.png")

    for imgfile in files:
        img = load_img(imgfile, target_size=(hw["height"], hw["width"]))    # �摜�t�@�C���̓ǂݍ���
        array = img_to_array(img) / 255                                     # �摜�t�@�C����numpy��
        arrlist.append(array)                 # numpy�^�f�[�^�����X�g�ɒǉ�
        for i in range(var_amount-1):
            arr2 = array
            arr2 = random_rotation(arr2, rg=360)
            arrlist.append(arr2)              # numpy�^�f�[�^�����X�g�ɒǉ�
        num += 1

    nplist = np.array(arrlist)
    np.save(filename, nplist)
    print(">> " + dirname + "����" + str(num) + "�̃t�@�C���ǂݍ��ݐ���")


################################
######### ���f���̍\�z #########
################################
def BuildCNN(ipshape=(32, 32, 3), num_classes=1):
    model = Sequential()

    model.add(Conv2D(24, 3, padding='same', input_shape=ipshape))
    model.add(Activation('relu'))

    model.add(Conv2D(48, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Conv2D(96, 3, padding='same'))
    model.add(Activation('relu'))

    model.add(Conv2D(96, 3))
    model.add(Activation('relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.5))

    model.add(Flatten())
    model.add(Dense(128))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))

    model.add(Dense(num_classes))
    model.add(Activation('softmax'))

    adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=1e-08)
    model.compile(loss='categorical_crossentropy',
                  optimizer=adam,
                  metrics=['accuracy'])
    return model


################################
############# �w�K #############
################################
def Learning(tsnum=30, nb_epoch=80, batch_size=8, learn_schedule=0.9):
    X_TRAIN_list = []; Y_TRAIN_list = []; X_TEST_list = []; Y_TEST_list = [];
    target = 0
    for filename in FileNames :
        data = np.load(filename)          # �摜��numpy�f�[�^��ǂݍ���
        trnum = data.shape[0] - tsnum
        X_TRAIN_list += [data[i] for i in range(trnum)]          # �摜�f�[�^
        Y_TRAIN_list += [target] * trnum                         # ���ޔԍ�
        X_TEST_list  += [data[i] for i in range(trnum, trnum+tsnum)]          # �w�K���Ȃ��摜�f�[�^
        Y_TEST_list  += [target] * tsnum;                                     # �w�K���Ȃ����ޔԍ�
        target += 1

    X_TRAIN = np.array(X_TRAIN_list + X_TEST_list)    # �A��
    Y_TRAIN = np.array(Y_TRAIN_list + Y_TEST_list)    # �A��
    print(">> �w�K�T���v���� : ", X_TRAIN.shape)
    y_train = np_utils.to_categorical(Y_TRAIN, target)    # ���R�����x�N�g���ɕϊ�
    valrate = tsnum * target * 1.0 / X_TRAIN.shape[0]

    # �w�K���̕ύX
    class Schedule(object):
        def __init__(self, init=0.001):      # �����l��`
            self.init = init
        def __call__(self, epoch):           # ���ݒl�v�Z
            lr = self.init
            for i in range(1, epoch+1):
                lr *= learn_schedule
            return lr

    def get_schedule_func(init):
        return Schedule(init)

    lrs = LearningRateScheduler(get_schedule_func(0.001))
    mcp = ModelCheckpoint(filepath='best.hdf5', monitor='val_loss', verbose=1, save_best_only=True, mode='auto')
    model = BuildCNN(ipshape=(X_TRAIN.shape[1], X_TRAIN.shape[2], X_TRAIN.shape[3]), num_classes=target)

    print(">> �w�K�J�n")
    hist = model.fit(X_TRAIN, y_train,
                     batch_size=batch_size,
                     verbose=1,
                     epochs=nb_epoch,
                     validation_split=valrate,
                     callbacks=[lrs, mcp])

    json_string = model.to_json()
    json_string += '##########' + str(ClassNames)
    open('model.json', 'w').write(json_string)
    model.save_weights('last.hdf5')


################################
########## ���s�E���� ##########
################################
def TestProcess(imgname):
    acc_array = [20] * 3
    modelname_text = open("model.json").read()
    json_strings = modelname_text.split('##########')
    textlist = json_strings[1].replace("[", "").replace("]", "").replace("\'", "").split()
    model = model_from_json(json_strings[0])
    model.load_weights("last.hdf5")  # best.hdf5 �ő����ŏ��̃p�����[�^���g�p
    img = load_img(imgname, target_size=(hw["height"], hw["width"]))    
    TEST = img_to_array(img) / 255
    pred = model.predict(np.array([TEST]), batch_size=1, verbose=0)
    acc_array[0] = '{:.1%}'.format((pred[0][0]))
    acc_array[1] = '{:.1%}'.format((pred[0][1]))
    acc_array[2] = '{:.1%}'.format((pred[0][2]))
    print(">> ��@�̐f�f���� �� �ʏ�:%s�A�\��:%s�A�̏�:%s" % (acc_array[0], acc_array[2], acc_array[1]))
    #print(">> ���̐�@�̐U���́u" + textlist[np.argmax(pred)].replace(",", "") + "�v�ł��B")
