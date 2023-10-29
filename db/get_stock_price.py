# import main libraries
import pandas as pd # data manipulation
import numpy as np # data manipulation
import yfinance as yf # get financials of the companies
import pymongo # connect to MongoDB
from pymongo import MongoClient # connect to MongoDB
import json # convert data to json


class Get_all_stock_price:
    def __init__(self,symboles:list, start,end):
        self.symboles = symboles
        self.start = start
        self.end = end
        
    def extract_ticker(self, symbol):
        date_ = list()
        open_= list()
        high= list()
        low= list()
        close= list()
        volume= list()
        df = None
        try:
            if yf.utils.is_valid_timezone(yf.Ticker(symbol)._fetch_ticker_tz(proxy=None, timeout=30)) == True:
                ticket = yf.Ticker(symbol)
                print('loading data')
                data = ticket.history(interval='1d', start=self.start, end=self.end)
                if len(data) > 0:
                    data.reset_index(inplace=True)
                    data.drop(['Dividends','Stock Splits'], axis=1, inplace=True)
                    data['Date'] =  pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
                    for i in range(len(data)):
                        date_.append(data.Date[i])
                        open_.append(data.Open[i])
                        high.append(data.High[i])
                        low.append(data.Low[i])
                        close.append(data.Close[i])
                        volume.append(data.Volume[i])
                        # create a dictionary to store the data
                    dct2 = {'Date': date_,
                                'Open': open_,
                                'High': high,
                                'Low': low,
                                'Close': close,
                                'Volume': volume }
                    # create a dataframe to store the data
                    df = pd.DataFrame(dct2)
                else:
                    pass
        except print(0):
            pass
        return df
    
    def transform_data(self, symbol):
        try:
            # create a dataframe to store the data
            df_transformed = self.extract_ticker(symbol) # call the extract function
            if df_transformed is not None:
                # convert the dataframe into a json file
                json_file = df_transformed.to_json('Data/yahoo_data_history.json' ,indent=4, orient='records')
                # load the json file into mongodb
                # create a client object
                connection_string = "mongodb://localhost:27017"
                client = pymongo.MongoClient(connection_string)
                #client = MongoClient('mongodb+srv://USER:PASSWORD@cluster0.ragcpnf.mongodb.net/?retryWrites=true&w=majority') # insert your connection string and your personal user and password of your MongoDB account
                # get a database named "stockdb"
                db1 = client.MemoireEsgf
                # get a collection named "yahoo_data_test_json"
                symbol_ = "_".join([symbol]).replace(" ", "_")
                symbol_ = "_".join([symbol]).replace(".", "_")
                print(symbol_)
                collection_main = db1[symbol_]
                # load a json file into mongodb
                with open('Data/yahoo_data_history.json') as file:
                    file_data = json.load(file)
                # insert_many is used else insert_one is used
                if isinstance(file_data, list):
                    # empty the collection
                    collection_main.delete_many({})
                    # insert the data into the collection
                    collection_main.insert_many(file_data)
                else:
                    collection_main.insert_one(file_data)
            else:
                pass
        except print(0):
            pass
        return True
    
    def get_hystoric(self):
        # call the extract function
        #extract_ticker()
        # call the transform function
        for symbol in self.symboles:
            self.transform_data(symbol)
            #time.sleep(2)
        return True