import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM,Dense
from keras.models import load_model
from tensorflow.keras.callbacks import ModelCheckpoint, CSVLogger
import pymongo


print("==================================PREPROCESSING=======================================")

#connection_string = "mongodb://localhost:27017"
#client = pymongo.MongoClient(connection_string)
#db = client.MemoireIndiceMarket
#collection = db.CAC_40

class Preprocess:

    def __init__(self, db, client, collection):
        self.db = db
        self.client = client
        self.collection = collection
        self.DataBase = self.client[self.db]
        self.collection = self.DataBase[self.collection]
        self.df = pd.DataFrame(list(self.collection.find()))
        self.data = self.df.drop('_id', axis=1)
        
    def prepocessing(self, df):
        df_ = df[['Date','Close']]
        data = df.filter(['Close']) 
        dataset = data.values.reshape(-1, 1)
        #training_data_len = int(np.ceil(len(dataset) * .8 ))
        #print(f'Longueur du data: {training_data_len}')
        print('================================================')
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data= scaler.fit_transform(dataset)
        train_data = scaled_data
        x_train = []
        y_train = []
        # Préparation des séquences temporelles
        sequence_length = 40
        #for i in range(40, len(train_data)):
        for i in range(len(train_data) - sequence_length):
            x_train.append(train_data[i:i+sequence_length])
            y_train.append(train_data[i+sequence_length])   # =====> revoir Y a predire 

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        print('PREPROCESSING DONE')
        print('================================================')
        return x_train, y_train, scaler, data, dataset, df_
    
        
    def split_data(self, df):
        data = df.filter(['Close']) 
        dataset = data.values.reshape(-1, 1)
        training_data_len = int(np.ceil(len(dataset) * .8 ))
        print(f'Longueur du data: {training_data_len}')
        print('================================================')
        scaler = MinMaxScaler(feature_range=(0,1))
        scaled_data= scaler.fit_transform(dataset)
        train_data = scaled_data[0:int(training_data_len), :]
        x_train = []
        y_train = []
        for i in range(40, len(train_data)):
            x_train.append(train_data[i-40:i, 0])
            y_train.append(train_data[i, 0])

        x_train, y_train = np.array(x_train), np.array(y_train)
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        test_data = scaled_data[training_data_len - 40: , :]
        x_test = []
        y_test = dataset[training_data_len:, :]
        for i in range(40, len(test_data)):
            x_test.append(test_data[i-40:i, 0])
        x_test = np.array(x_test)
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))
        return x_train, y_train, x_test, y_test, scaler, data, dataset, df, training_data_len
    
    def prep_data(self):
        data = self.data
        x_train, y_train, scaler, data, dataset, df = self.prepocessing(data)
        #x_train, y_train, x_test, y_test, scaler, data, dataset, df, training_data_len = self.split_data(data)
        return x_train, y_train, scaler, data, dataset, df 