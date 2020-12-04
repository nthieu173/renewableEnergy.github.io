from matplotlib import pyplot as plt
import pandas as pd
import numpy as np

from tensorflow import keras
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Input, Dense, Dropout, LeakyReLU
from tensorflow.keras.regularizers import l2
from tensorflow.keras.optimizers import Adam, SGD
from keras.callbacks import ModelCheckpoint
from keras.models import load_model

from sklearn.preprocessing import StandardScaler

def main(train_data_path, val_data_path, save_path, resume=False):
    train_data = pd.read_csv(train_data_path)
    val_data = pd.read_csv(val_data_path)
    
    x, y = preprocess_data(train_data)
    val_x, val_y = preprocess_data(val_data)
    if not resume:
        create_train_save(x, y, val_x, val_y, save_path)
    model = load_model(save_path)
    visualize_prediction(model, x, y)
    visualize_prediction(model, val_x, val_y)

def create_train_save(x, y, val_x, val_y, save_path):
    model = compile_model(input_length=x.shape[1], h_list=[128]*16, \
                          dropout_rate=0.2, l2_reg=1e-5, lr=5e-4)
    model, train_loss, val_loss = train(model, x, y, val_x, val_y, save_path, \
                                        bs=25, epochs=2000)
    plot_loss(train_loss, val_loss)

def visualize_prediction(model, x, y):
    scaler = StandardScaler()
    predictions = np.array(model.predict(x))
    error = np.abs(y - predictions)
    print(error)
    print(error.min(), error.max())
    print(error.mean(axis=None))

def drop_output_col(data):
    return data[data.columns.drop(['State','Year','average_electricity_price'])]

def preprocess_data(data):
    scaler = StandardScaler()

    x = drop_output_col(data)
    y = data['average_electricity_price']

    x = np.array(scaler.fit_transform(x))
    y = np.array(y)
    return x, y

def compile_model(input_length, h_list, dropout_rate, l2_reg, lr, loss='MSE'):
    model = keras.Sequential()
    model.add(Input((input_length,)))
    for h in h_list:
        model.add(Dense(h, kernel_regularizer=l2(l2_reg)))
        model.add(LeakyReLU(alpha=0.3))
        if dropout_rate > 0:
            model.add(Dropout(dropout_rate))
    model.add(Dense(1))
    opt = Adam(learning_rate=lr, beta_1=0.99,beta_2=0.999, amsgrad=True)
    model.compile(loss=loss, optimizer=opt)
    return model

def train(model, x, y, val_x, val_y, save_path, bs, epochs):
    bestValCheckpointer = ModelCheckpoint(save_path, monitor='val_loss', save_best_only=True, verbose=1)
    model.fit(x, y,  validation_data=(val_x, val_y), epochs=epochs, \
                   batch_size=bs, shuffle=True, callbacks=[bestValCheckpointer])
    history = model.history.history
    val_loss = history['val_loss']
    train_loss = history['loss']
    return model, val_loss, train_loss

def plot_loss(train_loss, val_loss):
    epochs = len(train_loss)
    plt.figure()
    plt.title('Loss Curves')
    plt.xlabel('Epochs')
    plt.ylabel('MSE Loss')
    plt.semilogy(np.arange(epochs), train_loss, label='Train Loss')
    plt.semilogy(np.arange(epochs), val_loss, label='Val Loss')
    plt.legend(loc='best')
    plt.show()

if __name__ == "__main__":
    main("./shuffled_consolidated_data_1998_to_2016.csv", \
         "./new_consolidated_data_2017_to_2019.csv", \
         #"./model_all")
         "./model_deep_4.477", resume=True)