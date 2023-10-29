import pymongo
import pandas as pd
from pathlib import Path  
import os


indices = {
    'Swiss Market' : '^SSMI', 
    'FTSE 100' : '^FTSE',
    'Euro Stoxx 50' : '^STOXX50E',
    'Dow Jones Industrial Average' : '^DJI',
    'S&P 500' : '^GSPC',
    'Nikkei 225' : '^N225',
    'Hang Seng Index' : '^HSI',
    'CAC 40' : '^FCHI',
    'DAX' : '^GDAXI',
    #'Shanghai Composite Index' : '^SSEC',
    'SENSEX' : '^BSESN',
    'Bovespa' : '^BVSP',
    'ASX 200' : '^AXJO',
    'KOSPI' : '^KS11',
    'TASI' : '^TASI.SR',
    'IPC' : '^MXX',
}

connection_string = "mongodb://localhost:27017"
client = pymongo.MongoClient(connection_string)
data_name = 'IndiceMarketPred'
db = client[data_name]


for col in indices.keys():
    collection_name = "_".join([col]).replace(" ", "_")
    name_indice = collection_name + '_Pred'
    collection = db[name_indice]
    df = pd.DataFrame(list(collection.find()))
    data = df.drop('_id', axis=1)

    filepath = Path(f'data/{name_indice}.csv')  
    filepath.parent.mkdir(parents=True, exist_ok=True)  
    data.to_csv(filepath)
    print(data)