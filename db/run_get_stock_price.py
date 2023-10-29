from get_stock_price import Get_all_stock_price
from datetime import date
import pandas as pd


df = pd.read_csv('../INDICES.csv',sep=';')
df = df.drop(['Unnamed: 10', 'Unnamed: 11','Unnamed: 12', 'Unnamed: 13', 'Unnamed: 14'], axis=1)
symboles = []
for col in df.columns:
    if col == 'HSI':
        pass
    else:
        d_f = df[f'{col}'].dropna().values
        for i in d_f:
            symboles.append(i)
    #if col == 'SP500':
    #    d_f = df[f'{col}'].dropna().values
    #    for i in d_f:
    #        symboles.append(i)
    #if col == 'HSI':
    #    d_f = df[f'{col}'].dropna().values
    #    for i in d_f:
    #        symboles.append(i)
    #else:
    #    pass

print(symboles)
#symboles = ['AI.PA','ZION','ATO.PA'] #,'IBM','JNJ','MCD']
#start = '2016-01-03'
start = '2022-08-01'
#end = '2023-08-25'
end = date.today()

def main():
    # call the get hystoric function
    #extract_ticker()
    # call the transform function
    get_all_stock = Get_all_stock_price(symboles, start, end)
    get_all_stock.get_hystoric()
    # call the load function
    return True

### Run Layer ###

if __name__ == '__main__':
    main()
    print('Data has been extracted, transformed, saved in a json file and loaded into mongodb')