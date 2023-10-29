from preprocessing import Preprocess
from datetime import date
import pymongo
from models import Model


connection_string = "mongodb://localhost:27017"
client = pymongo.MongoClient(connection_string)
data_name = 'MemoireIndiceMarket'
collection = 'Swiss_Market'
params = {
    'batch_size':16,
    'epochs':2,
    'validation_split': 0.1,
    'callbacks' : 'callbacks'
}
#symboles = ['MSFT','ZION','IBM','JNJ','MCD']

def main():
    # call the get hystoric function
    #extract_ticker()
    # call the transform function
    preprocess = Preprocess(data_name, client, collection)
    x_train, y_train, x_test, y_test, scaler, data, dataset, training_data_len  = preprocess.prep_data()
    #print(x_train)
    all_data = {
        'x_train': x_train, 
        'y_train': y_train, 
        'x_test': x_test, 
        'y_test': y_test, 
        'scaler': scaler, 
        'data': data, 
        'dataset': dataset, 
        'training_data_len': training_data_len 
    }
    model = Model(all_data, params, collection)
    model, history , valid = model.run_model()

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