from flask import Flask, jsonify, request, render_template
from flask_restful import Resource, Api, reqparse
import numpy as np
import pandas as pd
import requests
import pymongo
import json
import os
import time


# import dataset
################### ptf_non_equipondere
    
def get_data(name):
    connection_string = "mongodb://localhost:27017"
    client = pymongo.MongoClient(connection_string)
    db = client['Portefeuille']
    collection_main = db[f'{name}']
    df = pd.DataFrame(list(collection_main.find()))
    #print(df)
    if len(df) == 0:
        return None
    else:
        df = df.drop('_id', axis=1)
        df['Performance'] = round(((df['Valorisation']-df['Capital Investi'])/df['Capital Investi'])*100, 2)
        if 'Beta' in df.columns:
            df['Beta'] = round(df['Beta'], 2)
        data = {}
        for col in df.columns:
            #print(col)
            data[f'{col}'] = list(df[f'{col}'].values)
    return data

collection_name = ['ptf_equipondere','ptf_non_equipondere','ptf_traditionnel']
portefeuilles = []
for ptf in collection_name:
    #print('ptffffffffffff', ptf)
    df = get_data(ptf)
    portefeuilles.append(df)

valorisation_ptf = {}
for i in range(len(portefeuilles)):
    valorisation = round(sum(portefeuilles[i]['Valorisation']), 2)
    print('valorisation' , valorisation)
    capital_investi = round(sum(portefeuilles[i]['Capital Investi']), 2)
    print('capital_investi' , capital_investi)
    gain_perte = round(valorisation - capital_investi, 2)
    valorisation_ptf[f'{i+1}'] = [valorisation, capital_investi, gain_perte]
    print(gain_perte)
print('valorisation_ptf', valorisation_ptf)

def cast_type(container, from_types, to_types):
    if isinstance(container, dict):
        return {cast_type(k, from_types, to_types): cast_type(v, from_types, to_types) for k, v in container.items()}
    elif isinstance(container, list):
        return [cast_type(item, from_types, to_types) for item in container]
    else:
        for f, t in zip(from_types, to_types):
            if isinstance(container, f): 
                return t(container)
        return container


app = Flask(__name__)

# route 
@app.route('/home', methods=['GET'])
def index():
    url = request.args.get('url') 
    number = 1
    if url == None:
        number = number
    elif url == "http://api/portefeuilles/2":
        number = 2
    elif url == "http://api/portefeuilles/3":
        number = 3
    #dernier_caractere = url[-1]
    #print('URLLLLLLLLLLLLLLLLLL', url)             
    api_url =  'http://'+ 'localhost:5000/' + 'api/portefeuilles/'+ str(number)   #http://localhost:5000/api/portefeuilles/1
    response = requests.get(api_url)
    dt = response.json()
    
    print('URL', url, 'Valorisation :', valorisation, 'GAIN PERTE :', gain_perte)

    if response.status_code == 200:
        data = response.json()
        return render_template('base.html', data=data, valorisation=valorisation_ptf,
                               capital_investi=capital_investi, gain_perte=gain_perte, number=number)
    else:
        return "Erreur lors de la récupération des données de l'API"

    # affichage
    #return render_template('base.html', title='home', portefeuilles = df)
@app.route('/process_url', methods=['GET'])
def process_url():
    url = request.args.get('url')
    print(f'URL reçue depuis le navigateur : {url}')
    return f'URL reçue : {url}'


@app.route('/api/portefeuilles/1')
def ptf_equipondere():
    data = portefeuilles[0]
    return json.dumps( cast_type(data, [np.int64, np.float64],[int,float]), indent=2)

@app.route('/api/portefeuilles/2')
def ptf_non_equipondere():
    data = portefeuilles[1]
    return json.dumps( cast_type(data, [np.int64, np.float64],[int,float]), indent=2)

@app.route('/api/portefeuilles/3')
def ptf_traditionnel():
    data = portefeuilles[2]
    return json.dumps( cast_type(data, [np.int64, np.float64],[int,float]), indent=2)


# create port
port = int(os.environ.get("PORT", 5000))

if __name__ == '__main__':
    app.run(host='localhost', debug=True, port=port)