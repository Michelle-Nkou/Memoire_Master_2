from sklearn.metrics import mean_absolute_error
import numpy as np
import pandas as pd
import pymongo
from pathlib import Path  
import os
import re



preds_file = 'predictions/'
beta_file = 'data_beta/'
all_beta = {}
fichiers_beta = os.listdir(beta_file)
df_beta = pd.DataFrame()
for fichier in fichiers_beta:
    elements = fichier.split('_')
    nom_company = '_'.join(elements[2:])
    nom_company_split = nom_company.split(".csv")[0]
    if fichier.endswith('.csv'):
        path_fichier = os.path.join(beta_file, fichier)
        df_beta = pd.read_csv(path_fichier)
        df_beta = df_beta.drop('Unnamed: 0', axis=1)
    fichiers_csv = os.listdir(preds_file)
    for file in fichiers_csv:
        nom_sans_extension = file.split(".csv")[0]
        elements = file.split('_')
        result = '_'.join(elements[1:])
        if result == nom_company:
            if fichier.endswith('.csv'):
                chemin_fichier = os.path.join(preds_file, file)
                df = pd.read_csv(chemin_fichier)
                df = df.drop('Unnamed: 0', axis=1)
                periode_sma = len(df)
                df['SMA'] = df['Predictions'].rolling(window=periode_sma).mean()
                dernier_prix = df['Predictions'].iloc[-1]
                derniere_sma = df['SMA'].iloc[-1]
                if nom_company_split == 'S&P_500' or nom_company_split == 'CAC_40':
                    if dernier_prix > derniere_sma:
                        tendance = 'haussière'
                        beta_posi = df_beta[df_beta[f'{nom_company_split}_Company_Beta'] > 0]
                        filepath = Path(f'investissement/beta_positif/return_stock_beta_pos_{nom_company_split}.csv')  
                        filepath.parent.mkdir(parents=True, exist_ok=True)  
                        beta_posi.to_csv(filepath)
                    elif dernier_prix < derniere_sma:
                        tendance = 'baissière'
                        beta_neg = df_beta[df_beta[f'{nom_company_split}_Company_Beta'] < 0]
                        filepath = Path(f'investissement/beta_negatif/return_stock_beta_neg_{nom_company_split}.csv')  
                        filepath.parent.mkdir(parents=True, exist_ok=True)  
                        beta_neg.to_csv(filepath)
                    else:
                        tendance = 'indécise'
                    print(f"La tendance est {tendance}")
                    #Calculez les EMA à court terme et à long terme