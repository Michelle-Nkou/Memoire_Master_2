import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import MinMaxScaler
from preprocessing import Preprocess
import yfinance as yf






class Prediction:
    def __init__(self, client, db_name_indice, db_name_stock, collection, path, ticket):
        self.client = client
        self.db_name_indice = db_name_indice
        self.db_name_stock = db_name_stock
        self.collection = collection
        self.path = path
        self.ticket = ticket
        self.preprocess = Preprocess(self.db_name_indice, self.client, self.collection)

    def get_stock(self):
        db = self.client[self.db_name_stock]
        coll = db[self.ticket]
        data = pd.DataFrame(list(coll.find()))
        #print(data)
        data = data.drop('_id', axis=1)
        return data

    def get_benchmark_pred(self):
        x, y, scaler, data_tr, dataset_tr, df_prep_tr  = self.preprocess.prep_data()
        return x, y, scaler, data_tr, dataset_tr, df_prep_tr
    
    def model_pred(self, x, y, scaler, df_prep_tr):
        #new_model = tf.keras.models.load_model('../lib/model/data/modeles/Euro_Stoxx_50_model.h5')
        new_model = tf.keras.models.load_model(self.path)
        print(new_model.summary())
        df_prep_tr = df_prep_tr[40:]
        predictions = new_model.predict(x)
        predictions = scaler.inverse_transform(predictions)
        y = scaler.inverse_transform(y)
        rmse = np.sqrt(np.mean(((predictions - y) ** 2)))
        benchmarch_pred = df_prep_tr
        benchmarch_pred['Predictions'] = predictions
        print('======================MES PREDICTION INDICE==================================')
        print(benchmarch_pred)
        return new_model, rmse, benchmarch_pred

    def calculate_beta(self, stock, benchmark):
        stock_returns = stock['Close'].pct_change().dropna()
        benchmark_returns = benchmark['Predictions'].pct_change().dropna()
        min_len = min(len(stock_returns), len(benchmark_returns))
        print("====================MIN======================")
        print(min_len)
        print("====================MIN======================")

        stock_returns = stock_returns[-min_len:]
        benchmark_returns = benchmark_returns[-min_len:]
        
        covariance = np.cov(stock_returns, benchmark_returns)[0][1]
        benchmark_variance = np.var(benchmark_returns)
        beta = covariance / benchmark_variance
        return beta

    def get_prediction(self):
        stock = self.get_stock()
        #stock = stock[40:]
        x, y, scaler, data_tr, dataset_tr, df_prep_tr = self.get_benchmark_pred()
        new_model, rmse, benchmarch_pred = self.model_pred(x, y, scaler, df_prep_tr)
        beta = self.calculate_beta(stock, benchmarch_pred)
        return benchmarch_pred, beta, rmse