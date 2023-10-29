
from get_indices import Get_all_indice
from datetime import date


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

symboles = [i for i in indices.values()]
train = False
test = False 
strat = 'strat'
try:
    if train == 'train':
        start = '2008-01-01'
        end = '2020-12-31'
    elif test == 'test':
        start = '2021-01-01'
        end = '2022-07-31'
    elif strat == 'strat':
        start = '2022-08-01'
        end = date.today()
except:
    pass

def main():
    # call the get hystoric function
    #extract_ticker()
    # call the transform function
    get_all_stock = Get_all_indice(symboles, indices,strat, start, end)
    get_all_stock.get_hystoric()
    # call the load function
    return True

### Run Layer ###
if __name__ == '__main__':
    main()
    print('Data has been extracted, transformed, saved in a json file and loaded into mongodb')
