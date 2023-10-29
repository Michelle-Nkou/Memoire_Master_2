import sys
import os
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from preprocessing import Preprocess
from datetime import date
import pymongo
from models import Model
from connexion.connect import client
import pandas as pd
import json
import time

DataBase_name_train = 'MemoireIndiceMarket_Train'
DataBase_name_test = 'MemoireIndiceMarket_Test'
collection = 'CAC_40'


params = {
    'batch_size':32,
    'epochs':150,
    'validation_split': 0.1,
    'callbacks' : 'callbacks'
}

def main():
    print("_________________________ CONNEXION TO THE DATABASE DONE _________________________")
    time.sleep(2)
    for col in indices.keys():
        
        print(f" _________________________ GET DATA FOR {col} _________________________ ")
        collection_name = "_".join([col]).replace(" ", "_")
        print(f" _________________________ DATA FOR {col} DONE _________________________ ")
        print(f" _________________________ PREPROCESSING DATA FOR {col} _________________________ ")
        preprocess_train = Preprocess(DataBase_name_train, client, collection_name)
        preprocess_test = Preprocess(DataBase_name_test, client, collection_name)
        x_train, y_train, scaler, data_tr, dataset_tr, df_prep_tr  = preprocess_train.prep_data()
        x_test, y_test, scaler_test, data_ts, dataset_ts, df_prep_ts  = preprocess_test.prep_data()
        print(f" _________________________ PREPROCESSING FOR {col} IS DONE ! _________________________ ")
        #print(x_train)
        all_data = {
            'x_train': x_train, 
            'y_train': y_train, 
            'x_test': x_test, 
            'y_test': y_test, 
            'scaler': scaler_test, 
            'data': data_ts,
            'dataset': df_prep_ts, 
        }
        model = Model(all_data, params, collection_name)
        model, history , valid = model.run_model()
        print(f" _________________________ TRAINNING MODEL FOR {collection_name} DATA _________________________ ")
        print(f" _________________________ SAVING MODEL {collection_name}_model.H5 DONE _________________________ ")
   
        index = valid.index
        true_obs = list()
        pred_obs = list()
        date_list = list()
        for i in index:
            date_list.append(valid.Date[i])
            true_obs.append(valid.Close[i])
            pred_obs.append(valid.Predictions[i])

        dict1 = {'true_obs': true_obs,
                    'pred_obs': pred_obs,
                    'date': date_list,
                   }
                   
        print("________________________________val_______________")
        print(valid)
        # create a dataframe to store the data
        df = pd.DataFrame(dict1)
        file_path = f'data/{collection_name}.json'
        json_file = df.to_json(file_path ,indent=4, orient='records')

        db = client.IndiceMarketPred
        name_indice= collection_name + '_Pred'
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


        
        print(f" _________________________ SAVING PREDICTON FOR {collection_name}_model.H5 MODEL DONE _________________________ ")
        print('---------------------------')
        print(valid)
        print('---------------------------')
        print(history)
    # call the load function
    return True

### Run Layer ###

if __name__ == '__main__':
    main()
    print('Data has been extracted, transformed, saved in a json file and loaded into mongodb')