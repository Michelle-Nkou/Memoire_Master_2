# import main libraries
import pandas as pd # data manipulation
import numpy as np # data manipulation
import yfinance as yf # get financials of the companies
import pymongo # connect to MongoDB
from pymongo import MongoClient # connect to MongoDB
import json # convert data to json
from datetime import date
import os



class Get_all_indice:
    def __init__(self,symboles:list,dict_indice, d, start,end):
        self.symboles = symboles
        self.dict_indice = dict_indice
        self.d = d
        self.start = start
        self.end = end
        
    def extract_ticker(self, symbol):
        date_ = list()
        open_= list()
        high= list()
        low= list()
        close= list()
        volume= list()
        ticket = yf.Ticker(symbol)
        data = ticket.history(interval='1d', start=self.start, end=self.end)
        data.reset_index(inplace=True)
        data['Date'] =  pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
        data = data[['Date','Open','High','Low','Close','Volume']]
        for i in range(len(data)):
            date_.append(data.Date[i])
            open_.append(data.Open[i])
            high.append(data.High[i])
            low.append(data.Low[i])
            close.append(data.Close[i])
            volume.append(data.Volume[i])
        dct2 = {'Date': date_,
                    'Open': open_,
                    'High': high,
                    'Low': low,
                    'Close': close,
                    'Volume': volume }
        df = pd.DataFrame(dct2)
        return df
    
    def get_keys_from_value(self, d, val):
        return [k for k, v in d.items() if v == val]
    
    def transform_data(self, symbol):
            # create a dataframe to store the data
        df_transformed = self.extract_ticker(symbol) # call the extract function
        # convert the dataframe into a json file
        file_path = 'data/yahoo_indice_history.json'
        json_file = df_transformed.to_json(file_path ,indent=4, orient='records')
        # load the json file into mongodb
        # create a client object
        connection_string = "mongodb://localhost:27017"
        client = pymongo.MongoClient(connection_string)
        #client = MongoClient('mongodb+srv://USER:PASSWORD@cluster0.ragcpnf.mongodb.net/?retryWrites=true&w=majority') # insert your connection string and your personal user and password of your MongoDB account
        # get a database named "stockdb"
        try:
            if self.d == 'train':
                db = client.MemoireIndiceMarket_Train
            elif self.d == 'test':
                db = client.MemoireIndiceMarket_Test
            elif self.d == 'strat':
                db = client.MemoireIndiceMarket_Strat
        except print(0):
            pass
        # get name indice
        keys = self.get_keys_from_value(self.dict_indice, symbol)
        name_indice = "_".join(keys).replace(" ", "_")
        print(name_indice)
        # get a collection named "yahoo_data_test_json"
        collection_main = db[name_indice]
        # load a json file into mongodb
        with open(file_path) as file:
            file_data = json.load(file)
        # insert_many is used else insert_one is used
        if isinstance(file_data, list):
            # empty the collection
            collection_main.delete_many({})
            # insert the data into the collection
            collection_main.insert_many(file_data)
        else:
            collection_main.insert_one(file_data)
            
        os.remove(file_path)
        return True
    
    def get_hystoric(self):
        # call the extract function
        #extract_ticker()
        # call the transform function
        for symbol in self.symboles:
            self.transform_data(symbol)
        return True