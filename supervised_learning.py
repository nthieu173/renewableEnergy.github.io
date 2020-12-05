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

def main(train_data_path, val_data_path, viz_data_path, save_path, resume=False, train=True):
    train_data = pd.read_csv(train_data_path)
    val_data = pd.read_csv(val_data_path)
    
    x, y = preprocess_data(train_data)
    val_x, val_y = preprocess_data(val_data)
    if resume:
        model = load_model(save_path)
    else:
        model = compile_model(input_length=x.shape[1], h_list=[128]*16, \
                              dropout_rate=0.2, l2_reg=2e-5, lr=1e-3)
                
    if train:
        train_save(model, x, y, val_x, val_y, save_path)
    model = load_model(save_path)

    viz_data = pd.read_csv(viz_data_path)
    visualize_prediction(model, viz_data)

def train_save(model, x, y, val_x, val_y, save_path):
    model, train_loss, val_loss = train(model, x, y, val_x, val_y, save_path, \
                                        bs=25, epochs=1000)
    plot_loss(train_loss, val_loss)

def visualize_prediction(model, data):
    x, y = preprocess_data(data)
    predictions = pd.DataFrame(model.predict(x))
    data['prediction'] = predictions
    states = pd.unique(data['State'])
    fig, axs = plt.subplots(10,5,figsize=(15,45))
    for state, ax in zip(states, axs.flat):
        state_data = data[data['State'] ==  state]
        error = np.abs(state_data['average_electricity_price'] - state_data['prediction'])
        ax.set_title(state)
        ax.plot(state_data['Year'], error)
    fig.savefig('error_visualization.svg', bbox_inches="tight")
    fig.savefig('error_visualization.png', bbox_inches="tight")


def drop_output_col(data):
    return data[data.columns.drop(['State','Year','average_electricity_price'])]

def preprocess_data(data):
    scaler = StandardScaler()

    x = drop_output_col(data)
    y = data['average_electricity_price']

    x = np.array(scaler.fit_transform(x))
    y = np.array(y).reshape(-1,1)
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
    opt = Adam(learning_rate=lr, beta_1=0.999,beta_2=0.999, amsgrad=True)
    model.compile(loss=loss, optimizer=opt)
    return model

def train(model, x, y, val_x, val_y, save_path, bs, epochs):
    bestValCheckpointer = ModelCheckpoint(save_path, monitor='val_loss', save_best_only=True, verbose=1)
    model.fit(x, y,  validation_data=(val_x, val_y), epochs=epochs, \
                   batch_size=bs, shuffle=True, callbacks=[bestValCheckpointer])
    history = model.history.history
    return model, history['loss'], history['val_loss']

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
         "./consolidated_data_2017_to_2019.csv", \
         "./consolidated_data_1998_to_2019.csv", \
         #save_path="./model_all")
        "./model_deep_3.98", resume=True, train=False)