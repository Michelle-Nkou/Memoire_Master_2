from preprocessing import Preprocess
from datetime import date
import pymongo
from models import Model
from beta import Prediction
import pandas as pd
import os
from pathlib import Path  



connection_string = "mongodb://localhost:27017"
client = pymongo.MongoClient(connection_string)
db = client.MemoireEsgf
# Obtenez la liste de toutes les collections dans la base de données
collection_list = db.list_collection_names()
#print("Liste de collections :", collection_list)


df = pd.read_csv('../INDICES.csv',sep=';')
df = df.drop(['Unnamed: 10', 'Unnamed: 11','Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14'], axis=1)
components = {}
for col in df.columns:
    if col != 'HSI':
        components["_".join([col]).replace(" ", "_")] = df[f'{col}'].dropna().values
    else:
        pass

for indice, list_ticket in components.items():
    listes = []
    listes.clear()
    for i in list_ticket:
        val = "_".join([i]).replace(".", "_")
        val = "_".join([val]).replace(" ", "_")
        listes.append(val)
    components[indice] = [i for i in listes if i in collection_list]
        #for i in df[f'{col}'].dropna().values:
        #    val = "_".join([i]).replace(".", "_")
        #    val = "_".join([val]).replace(" ", "_") 
        #    #print(list_val)
        #    if val in collection_list:
        #        #print(val)
        #        list_val.append(val)
            #print(list_val)
    #print(list_val)
        #components["_".join([col]).replace(" ", "_")] = list_val

#collection_name = "_".join([col]).replace(" ", "_")

#data_name = 'MemoireIndiceMarket'
#indice = 'Euro_Stoxx_50'
db_name_indice = 'MemoireIndiceMarket_Strat'
db_name_stock = 'MemoireEsgf'
#collection = 'Euro_Stoxx_50'
path_model = 'model/data/modeles/Euro_Stoxx_50_model.h5'
ticket  = 'AI_PA'

print('components', components)
#components= {'SP500': ['MMM'], 'CAC40': ['RI_PA'], 'Swiss_Market': ['ZURN_SW'], 'FTSE_100': ['ABDN_L'],
# 'Euro_Stoxx_50': ['DPW_DE'], 'IPC': ['IENOVA_MX']}

def main():
    d={}
    #df = pd.DataFrame()
    components.pop('SP500')
    components.pop('CAC40')
    components.pop('DAX')
    components.pop('SENSEX')
    components.pop('ASX')
    components.pop('Swiss_Market')
    components.pop('FTSE_100')
    components.pop('Euro_Stoxx_50')
    components.pop('IPC')
    print(components)
    for indice, list_tickets in components.items():
        list_beta = []
        list_ticket = []
        list_beta.clear()
        #list_beta.clear()
        if indice == 'SP500':
            indice = 'S&P_500'
            path_model = f'model/data/modeles/{indice}_model.h5'
        elif indice == 'CAC40':
            indice = 'CAC_40'
            path_model = f'model/data/modeles/{indice}_model.h5'
        else:
            path_model = f'model/data/modeles/{indice}_model.h5'
        for ticket in list_tickets:
            prediction = Prediction(client, db_name_indice, db_name_stock, indice, path_model, ticket)
            benchmarch_pred, beta, rmse  = prediction.get_prediction()
            print('beta', beta)
            print('rmse', rmse)
            list_beta.append(beta)
            list_ticket.append(ticket)
            if ticket == list_tickets[-1]:
                filepath2 = Path(f'predictions/pred_{indice}.csv')  
                filepath2.parent.mkdir(parents=True, exist_ok=True)  
                benchmarch_pred.to_csv(filepath2) 
            #print(len(list_beta))
            #print(len(list_ticket))
        d[f'{indice}'] = list_ticket
        d[f'{indice}_Company_Beta'] = list_beta
        df = pd.DataFrame(data=d)
        filepath = Path(f'data_beta/Beta_Company_{indice}.csv')  
        filepath.parent.mkdir(parents=True, exist_ok=True)  
        df.to_csv(filepath) 
    ##
    print(f'========================================{indice} DONE ====================================================')
    #print(df)
            #print(benchmarch_pred)
            #print('--------------beta-------------')
            #print(beta)
            #print('--------------rmse-------------')
            #print(rmse)
            # call the load function
    return True

### Run Layer ###

if __name__ == '__main__':
    main()
    print('Data has been extracted, transformed, saved in a json file and loaded into mongodb')