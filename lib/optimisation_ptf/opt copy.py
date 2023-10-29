#from projet.lib.beta import Prediction
from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd
import pymongo
from pathlib import Path  
from datetime import datetime
import os
import re


connection_string = "mongodb://localhost:27017"
client = pymongo.MongoClient(connection_string)
db = client['MemoireEsgf']

# Spécifiez le chemin du dossier contenant les fichiers CSV
preds_file = 'predictions/'
beta_file = 'data_beta/'

all_beta = {}
fichiers_beta = os.listdir(beta_file)
df_beta = pd.DataFrame()
for fichier in fichiers_beta:
    elements = fichier.split('_')
    nom_company = '_'.join(elements[2:])
    #indice_point = fichier.index('.')
    #indice_trait_soulignement = fichier.rindex('_')
    #resultat = fichier[indice_trait_soulignement + 1 : indice_point]
    #print('fichier',fichier)
    nom_company_split = nom_company.split(".csv")[0]
    print('MARCHE :',nom_company)
    if fichier.endswith('.csv'):
        path_fichier = os.path.join(beta_file, fichier)
        df_beta = pd.read_csv(path_fichier)
        df_beta = df_beta.drop('Unnamed: 0', axis=1)
        #print(df_beta)
        print("#########################")
        #for col in df.columns:
        #    all_beta[nom_company] = df[f'{col}'].dropna().values

    # Obtenez la liste des fichiers dans le dossier
    fichiers_csv = os.listdir(preds_file)
    for file in fichiers_csv:
        nom_sans_extension = file.split(".csv")[0]
        elements = file.split('_')
        result = '_'.join(elements[1:])
        print('result',result)
        if result == nom_company:
            print('######### BETA COMPANY ##########')
            print(df_beta.head())
            if file.endswith('.csv'):
                chemin_file = os.path.join(preds_file, file)
                df = pd.read_csv(chemin_file)
                df = df.drop('Unnamed: 0', axis=1)
                print('######### DATA PREDICTION ##########')
                #print(df)
                mae = mean_absolute_error(df.Close, df.Predictions)
                print(f"Mean Absolute Error (MAE): {mae}")
                periode_ema_long = 20  # 10 mois
                df['Date'] = pd.to_datetime(df['Date'])
                df.set_index('Date', inplace=True)
                df['EMA_Long'] = df['Predictions'].ewm(span=periode_ema_long).mean()
                data_monthly = df.resample('M').last()
                print('ENTREPRISE' , nom_sans_extension)
                for index, row in data_monthly.iterrows():
                    print('index', index)
                    date = index.strftime('%Y-%m-%d')
                    dernier_prix = row['Predictions']
                    print('dernier_prix', dernier_prix)
                    # ema_court = row['EMA_Court']
                    ema_long = row['EMA_Long']
                    print('ema_long', ema_long)
                    if dernier_prix > ema_long:
                        date_formatee = index.strftime('%Y-%m-%d')
                        print(date_formatee)
                        for i in df_beta[f'{nom_company_split}'].values:
                            collection = db[f'{i}']
                            df_ = pd.DataFrame(list(collection.find()))
                            df_ = df_.drop('_id', axis=1)
                        print('============================')
                        #print(df_)
                        if len(df_[df_['Date'] == date_formatee ]['Close'].values) > 0:
                            val = df_[df_['Date'] == date_formatee ]['Close'].values[0]
                        else:
                            val = 0
                        print('============================')
                        print(val)
                        print('============================')
                        tendance = 'haussière'
                        beta_posi = df_beta[df_beta[f'{nom_company_split}_Company_Beta'] > 0]
                        beta_posi['Tendance'] = 'Haussiere'
                        beta_posi['Periode'] = date_formatee
                        index = df_[df_['Date'] == date_formatee ]['Close'].index
                        beta_posi['Prix'] = val
                        print(beta_posi)
                        filepath = Path(f'investissement/beta_positif/return_stock_beta_pos_{nom_company_split}_{date_formatee}.csv')  
                        filepath.parent.mkdir(parents=True, exist_ok=True)  
                        beta_posi.to_csv(filepath) 
                    elif dernier_prix < ema_long:
                        date_formatee = index.strftime('%Y-%m-%d')
                        print(date_formatee)
                        for i in df_beta[f'{nom_company_split}'].values:
                            collection = db[f'{i}']
                            df_ = pd.DataFrame(list(collection.find()))
                            df_ = df_.drop('_id', axis=1)
                        tendance = 'baissière'
                        if len(df_[df_['Date'] == date_formatee ]['Close'].values) > 0:
                            val = df_[df_['Date'] == date_formatee ]['Close'].values[0]
                        else:
                            val = 0
                        beta_neg = df_beta[df_beta[f'{nom_company_split}_Company_Beta'] < 0]
                        beta_neg['Tendance'] = 'Baissière'
                        beta_neg['Periode'] = date_formatee
                        beta_neg['Prix'] = val
                        print(beta_neg)
                        filepath = Path(f'investissement/beta_negatif/return_stock_beta_neg_{nom_company_split}_{date_formatee}.csv')  
                        filepath.parent.mkdir(parents=True, exist_ok=True)  
                        beta_neg.to_csv(filepath)
                    else:
                        tendance = 'indécise'
                    print(f"Tendance en {date}: {tendance}")


