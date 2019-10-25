# 0. package load
import numpy as np
import argparse
import os

from azureml.core import Run

import tensorflow as tf
import keras
from keras.models import Sequential, model_from_json
from keras.layers import Dense, Dropout, Activation, Flatten
from keras.layers import Conv2D, MaxPooling2D
from keras.optimizers import SGD
from keras.callbacks import Callback

import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

print("Keras version:", keras.__version__)
print("Tensorflow version:", tf.__version__)


# 1. AML parameter를 위한 parser
parser = argparse.ArgumentParser()
parser.add_argument('--data-folder', type=str, dest='data_folder', help='data folder mounting point')
parser.add_argument('--batch-size', type=int, dest='batch_size', default=50, help='mini batch size for training')
parser.add_argument('--epoch', type=int, dest='epoch', default=20, help='# of training')
parser.add_argument('--first-dropout', type=float, dest='drop_1', default=0.5,
                    help='% of dropout')
parser.add_argument('--second-dropout', type=float, dest='drop_2', default=0.5,
                    help='% of dropout')
parser.add_argument('--learning-rate', type=float, dest='learning_rate', default=0.001, help='learning rate')

args = parser.parse_args()

data_folder = args.data_folder
batch_size = args.batch_size
n_epochs = args.epoch
d1 = args.drop_1
d2 = args.drop_2
learning_rate = args.learning_rate

n_inputs = 32 * 32
n_outputs = 10


# 2. Data 준비
X = np.load(os.path.join(data_folder, 'images.npy')) / 255.0
y = np.load(os.path.join(data_folder, 'label.npy'))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

y_train = keras.utils.to_categorical(y_train, n_outputs)
y_test = keras.utils.to_categorical(y_test, n_outputs)
print(X_train.shape, y_train.shape, X_test.shape, y_test.shape, sep='\n')


# 3. CNN 모델 생성
model = Sequential()

model.add(Conv2D(8, (3, 3), input_shape=(32, 32, 3), padding='same', activation='relu'))
model.add(Dropout(d1))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dropout(d2))

model.add(Dense(n_outputs, activation='softmax'))

model.summary()

model.compile(loss='categorical_crossentropy',
              optimizer=SGD(lr=learning_rate),
              metrics=['accuracy'])


# 4. Azure ML 실행 🌟🌟🌟🌟🌟
run = Run.get_context()

class LogRunMetrics(Callback):
    # callback at the end of every epoch
    def on_epoch_end(self, epoch, log):
        # log a value repeated which creates a list
        run.log('Loss', log['loss'])
        run.log('Accuracy', log['accuracy'])


# 5. 학습
model.fit(X_train, y_train,
                   batch_size=batch_size,
                   epochs=n_epochs,
                   verbose=1,
                   validation_data=(X_test, y_test),
                   callbacks=[LogRunMetrics()])

score = model.evaluate(X_test, y_test, verbose=0)


# 6. 로그 출력
run.log("Final test loss", score[0])
print('Test loss:', score[0])

run.log('Final test accuracy', score[1])
print('Test accuracy:', score[1])


# 7. 생성된 모델 파일 저장하기
os.makedirs('./outputs/model', exist_ok=True)

model_json = model.to_json()
# model JSON
with open('./outputs/model/model.json', 'w') as f:
    f.write(model_json)
# model weights
model.save_weights('./outputs/model/model.h5')
print("model saved in ./outputs/model folder")
