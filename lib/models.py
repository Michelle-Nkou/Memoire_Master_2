import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_absolute_error
from keras.models import Sequential
from keras.layers import LSTM,Dense
from keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.model_selection import train_test_split
import csv



class Model:
    def __init__(self, data, params, symbol):
        self.data = data
        self.params = params
        self.symbol = symbol

    def algo_lstm(self, data):
        model = Sequential([
            LSTM(units=50, return_sequences=True, input_shape=(data['x_train'].shape[1], 1)),
            Dropout(0.2),
            LSTM(units=50, return_sequences=True),
            Dropout(0.2),
            #LSTM(units=50),
            #Dropout(0.2),
            Dense(1)  # Prédiction du prix de clôture
        ])
        checkpointer = ModelCheckpoint(filepath=f"data/modeles/{self.symbol}_model.h5", verbose=1, save_best_only=True)
        csv_logger = CSVLogger(f"data/historique/{self.symbol}_history_loss.log")
        callbacks=[csv_logger, checkpointer]

        model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mae'])
        history = model.fit(data['x_train'], data['y_train'], batch_size=self.params['batch_size'], epochs=self.params['epochs'], callbacks=[callbacks],
                  validation_split=self.params['validation_split'])
        
        loss = model.evaluate(data['x_test'], data['y_test'])
        #print('Loss:', loss)
        csv_filename = f'data/historique_test/{self.symbol}_test_loss.csv'
        with open(csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Loss on test data'])
            writer.writerow([loss])
        print('Loss on test data saved to', csv_filename)
        #model = Sequential()
        #model.add(LSTM(50, return_sequences=True, input_shape= (data['x_train'].shape[1], 1)))
        #model.add(LSTM(50, return_sequences= False))
        #model.add(Dense(25))
        #model.add(Dense(1))
        #checkpointer = ModelCheckpoint(filepath=f"data/modeles/{self.symbol}_model.h5", verbose=1, save_best_only=True)
        #csv_logger = CSVLogger(f"data/historique/{self.symbol}_history_loss.log")
        #callbacks=[csv_logger, checkpointer]
        #model.compile(optimizer='adam', loss='mean_squared_error')
        #history = model.fit(data['x_train'], data['y_train'], batch_size=self.params['batch_size'], epochs=self.params['epochs'],
        #                     validation_split=self.params['validation_split'], callbacks=[callbacks])

        #plt.plot(history.history['loss'])
        #plt.plot(history.history['val_loss'])
        #plt.title('model loss')
        #plt.ylabel('loss')
        #plt.xlabel('epoch')
        #plt.legend(['train', 'val'], loc='upper left')
        #plt.show()
        # GET TEST DATA

        predictions = model.predict(data['x_test'])
        predictions = data['scaler'].inverse_transform(predictions)

        rmse = np.sqrt(np.mean(((predictions - data['y_test']) ** 2)))
        # Calcul du MAE
        mae = mean_absolute_error(data['y_test'], predictions)
        # Affichage du MAE
        print(f"Mean Absolute Error (MAE): {mae}")
        print('================================================')
        print(f'RMSE: {rmse}')
        print('================================================')
        #train = data['data'][:data['training_data_len']]
        valid = data['dataset'][40:]
        #valid = data['data']
        valid['Predictions'] = predictions

        #plt.figure(figsize=(16,8))
        #plt.title('Prédictions vs. valeurs réeles')
        #plt.xlabel('Date', fontsize=18)
        #plt.ylabel('Close USD ($)', fontsize=18)
        #plt.plot(train['Close'])
        #plt.plot(valid[['Close', 'Predictions']])
        #plt.legend(['Train', 'Valeurs actuelles', 'Prédictions'], loc='lower right')
        #plt.show()
        print('================== PREDICTION =================')
        print(valid)

        return model, history , valid

    def run_model(self):
        data_params = self.data
        model, history , valid = self.algo_lstm(data_params)
        return model, history , valid

    #model = algo_lstm(x_train, y_train, x_test, y_test, scaler, "CAC_40")
