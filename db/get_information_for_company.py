# import main libraries
import pandas as pd # data manipulation
import numpy as np # data manipulation
import yfinance as yf # get financials of the companies
import pymongo # connect to MongoDB
from pymongo import MongoClient # connect to MongoDB
import json # convert data to json




class Get_info_stock:
    def __init__(self,symboles:list):
        self.symboles = symboles

    def extract_ticker(self, symbols):
        # extract the ticker data
        #dct2 = {}
        Company_name = list()
        Company_ticker= list()
        Closed_price= list()
        Company_info= list()
        Company_PE= list()
        Company_cash_flow= list()
        Company_dividend= list()
        for sym in symbols:
            ticket = yf.Ticker(sym)
            Company_name.append(ticket.info['longName'])
            Company_ticker.append(ticket.info['symbol'])
            Closed_price.append(ticket.info['previousClose'])
            Company_info.append(ticket.info['longBusinessSummary'])
            Company_PE.append(ticket.info['trailingPE'])
            Company_cash_flow.append(ticket.info['operatingCashflow'])
            Company_dividend.append(ticket.info['dividendRate'])
            # create a dictionary to store the data
        dct2 = {'Company_name': Company_name,
                    'Company_ticker': Company_ticker,
                    'Closed_price': Closed_price,
                    'Company_info': Company_info,
                    'Company_PE': Company_PE,
                    'Company_cash_flow': Company_cash_flow,
                    'Company_dividend': Company_dividend }
        # create a dataframe to store the data
        df = pd.DataFrame(dct2)
        # return the dataframe
        return df
    
    def transform_data(self):
        # create a dataframe to store the data
        df_transformed = self.extract_ticker(self.symboles) # call the extract function
        # round the values of the dataset to 2 decimal places
        df_transformed = df_transformed.round(2)
        # convert the dataframe into a json file
        json_file = df_transformed.to_json('Data/yahoo_data.json' ,indent=4, orient='records')
        return json_file
    
    def load_mongo(self):
        '''load the json file into mongodb
           create a client object
           - get a database named "stockdb"
           - get a collection named "yahoo_data_test_json"
           - load a json file into mongodb
           - insert_many is used else insert_one is used
           - empty the collection
           - insert the data into the collection
        '''
        
        connection_string = "mongodb://localhost:27017"
        client = pymongo.MongoClient(connection_string)
        db = client.FinanceDbStock
        collection_main = db.info_company
        with open('Data/yahoo_data.json') as file:
            file_data = json.load(file)
        if isinstance(file_data, list):
            collection_main.delete_many({})
            collection_main.insert_many(file_data)
        else:
            collection_main.insert_one(file_data)
        return True