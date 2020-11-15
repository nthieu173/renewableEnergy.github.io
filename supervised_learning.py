import os
from tqdm import tqdm
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout
# from tensorflow.keras.layers.advanced_activations import PReLU
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam, SGD
from keras.callbacks import ModelCheckpoint
from keras.models import load_model

from sklearn.model_selection import RepeatedKFold

class Model():
    def __init__(self, data_path, resume=False, model_path=None, epochs=500, lr=1e-3):
        self.base_dir = os.getcwd()
        self.data_path = data_path
        self.resume = resume
        self.model_path = model_path
        self.model_folder = os.path.join(self.base_dir, 'model')
        self.epochs = epochs
        self.lr = lr


    def preprocess_data(self):
        data = pd.read_csv(self.data_path)
        df_x = data[data.columns.drop(['State','Year','average_electricity_price'])]
        df_y = data['average_electricity_price']
        self.x = np.array(df_x)
        self.y = np.array(df_y)
        self.num_data, self.features = self.x.shape


    def compile_model(self, h1=512, h2=256, dropout=True, dropout_rate=0.1, l2_reg=0.01, loss='mse', optimizer='Adam'):
        if not self.resume:
            input_shape = self.features
            self.model = keras.Sequential()
            self.model.add(Input((input_shape,)))
            self.model.add(Dense(h1, activation='selu', kernel_regularizer=l2(l2_reg)))
            if dropout:
                self.model.add(Dropout(dropout_rate))
            self.model.add(Dense(h2, activation='selu', kernel_regularizer=l2(l2_reg)))
            if dropout:
                self.model.add(Dropout(dropout_rate))
            self.model.add(Dense(1, activation='relu'))


            print('Model Initialized')

        else:
            self.model = load_model(self.model_path)
            print(f'Model Loaded from {self.model_path}')

        if optimizer == 'Adam':
            opt = Adam(learning_rate=self.lr)
        elif optimizer == 'SGD':
            opt = SGD(learning_rate=self.lr)
        else:
            opt = optimizer

        self.model.compile(loss=loss, optimizer=opt)
        print('Model Compiled')


    def train(self, vsplit=0.2, bs=50):
        bestValCheckpointer = ModelCheckpoint(os.path.join(self.model_folder, 'model_all.hdf5'), monitor='val_loss', save_best_only=True,
                                                     verbose=1)
        self.model.fit(self.x, self.y, epochs=self.epochs, batch_size=bs, validation_split=vsplit, callbacks=[bestValCheckpointer])
        self.history = self.model.history.history
        self.val_loss = self.history['val_loss']
        self.train_loss = self.history['loss']


    def plot_loss(self):
        plt.figure()
        plt.title('Loss Curves')
        plt.xlabel('Epochs')
        plt.ylabel('MSE Loss')
        plt.plot(np.arange(self.epochs), self.train_loss, label='Train Loss')
        plt.plot(np.arange(self.epochs), self.val_loss, label='Val Loss')
        plt.legend(loc='best')
        plt.show()


    def save(self, path):
        self.model.save(path)
        print(f'Model saved to {path}')


    def __call__(self):
        self.preprocess_data()
        self.compile_model()
        self.train()
        self.plot_loss()





