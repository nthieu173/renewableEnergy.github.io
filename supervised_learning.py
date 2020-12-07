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

import scipy.stats

def main(train_data_path, val_data_path, viz_data_path, save_path, resume=False, train=False):
    train_data = pd.read_csv(train_data_path)
    val_data = pd.read_csv(val_data_path)
    
    x, y = preprocess_data(train_data)
    val_x, val_y = preprocess_data(val_data)
    if resume:
        model = load_model(save_path)
    else:
        model = compile_model(input_length=x.shape[1], h_list=[128]*16, \
                              dropout_rate=0.2, l2_reg=1e-5, lr=5e-4)
    if train:
        train_save(model, x, y, val_x, val_y, save_path)
    model = load_model(save_path)

    viz_data = pd.read_csv(viz_data_path)
    v_x, v_y = preprocess_data(viz_data)
    predictions = pd.DataFrame(model.predict(v_x))
    viz_data['prediction'] = predictions

    visualize_prediction(model, viz_data)
    visualize_state_error(model, viz_data)
    visualize_year_error(model, viz_data)
    confidence_interval(model, viz_data)
    abs_confidence_interval(model, viz_data)

def train_save(model, x, y, val_x, val_y, save_path):
    model, train_loss, val_loss = train(model, x, y, val_x, val_y, save_path, \
                                        bs=25, epochs=2000)
    plot_loss(train_loss, val_loss)

def visualize_prediction(model, data):
    fig, axs = plt.subplots(10,5,figsize=(20,40))
    for state, ax in zip(pd.unique(data['State']), axs.flat):
        state_data = data[data['State'] ==  state]
        ax.set_title(state)
        ax.plot(state_data['Year'], state_data['average_electricity_price'])
        ax.plot(state_data['Year'], state_data['prediction'])
        ax.legend(["Truth", "Prediction"], loc="lower right")
    fig.savefig('state_prediction_visualization.svg', bbox_inches="tight")
    fig.savefig('state_prediction_visualization.png', bbox_inches="tight")


def visualize_state_error(model, data):
    fig, axs = plt.subplots(10,5,figsize=(20,40))
    for state, ax in zip(pd.unique(data['State']), axs.flat):
        state_data = data[data['State'] ==  state]
        error = state_data['prediction'] - state_data['average_electricity_price']
        rel_error = error / state_data['average_electricity_price']
        ax.set_title(state)
        ax.plot(state_data['Year'], rel_error)
        ax.axhline(y=np.mean(rel_error), color="r")
    fig.savefig('state_error_visualization.svg', bbox_inches="tight")
    fig.savefig('state_error_visualization.png', bbox_inches="tight")

def visualize_year_error(model, data):
    years = sorted(pd.unique(data['Year']))
    num_states = len(pd.unique(data['State']))
    mean_year_error = []
    for year in years:
        year_data = data[data['Year'] == year]
        error = np.abs(year_data['prediction'] - year_data['average_electricity_price'])
        rel_error = error / year_data['average_electricity_price']
        mean_year_error += [rel_error.sum() / num_states]
    fig = plt.figure()
    plt.plot(years, mean_year_error)
    plt.axhline(y=np.mean(mean_year_error), color="r")
    fig.savefig('year_error_visualization.svg', bbox_inches="tight")
    fig.savefig('year_error_visualization.png', bbox_inches="tight")

def confidence_interval(model, data, alpha = 0.05):
    states = pd.unique(data['State'])
    mean_state_error = np.zeros(len(states))
    c_intervals = np.zeros(len(states))
    for i, state in enumerate(states):
        state_data = data[data['State'] ==  state]
        error = state_data['prediction'] - state_data['average_electricity_price'] / state_data['average_electricity_price']
        n = len(state_data)
        t_alpha_2 = scipy.stats.t.isf(alpha/2, n-1) # t_{alpha/2}
        mean = error.mean()
        variance = np.square(error - mean).sum() / (n - 1)
        confidence = t_alpha_2*np.sqrt(variance/n)
        mean_state_error[i] = mean
        c_intervals[i] = confidence
    fig = plt.figure(figsize=(16,4))
    sorted_arg = np.argsort(mean_state_error)
    states = states[sorted_arg]
    c_intervals = c_intervals[sorted_arg]
    mean_state_error = mean_state_error[sorted_arg]
    plt.errorbar(states, mean_state_error, yerr=c_intervals, ecolor="orange")
    fig.savefig('state_confidence_error_visualization.svg', bbox_inches="tight")
    fig.savefig('state_confidence_error_visualization.png', bbox_inches="tight")

def abs_confidence_interval(model, data, alpha = 0.05):
    states = pd.unique(data['State'])
    mean_state_error = np.zeros(len(states))
    c_intervals = np.zeros(len(states))
    for i, state in enumerate(states):
        state_data = data[data['State'] ==  state]
        error = np.abs(state_data['prediction'] - state_data['average_electricity_price']) / state_data['average_electricity_price']
        n = len(state_data)
        t_alpha_2 = scipy.stats.t.isf(alpha/2, n-1) # t_{alpha/2}
        mean = error.mean()
        variance = np.square(error - mean).sum() / (n - 1)
        confidence = t_alpha_2*np.sqrt(variance/n)
        mean_state_error[i] = mean
        c_intervals[i] = confidence
    fig = plt.figure(figsize=(16,4))
    sorted_arg = np.argsort(mean_state_error)
    states = states[sorted_arg]
    c_intervals = c_intervals[sorted_arg]
    mean_state_error = mean_state_error[sorted_arg]
    plt.errorbar(states, mean_state_error, yerr=c_intervals, ecolor="orange")
    fig.savefig('state_confidence_abs_error_visualization.svg', bbox_inches="tight")
    fig.savefig('state_confidence_abs_error_visualization.png', bbox_inches="tight")

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
         "./consolidated_data_2017_to_2019.csv", \
         "./consolidated_data_1998_to_2019.csv", \
         #save_path="./model_all")
         "./model_3.98", resume=True, train=False)