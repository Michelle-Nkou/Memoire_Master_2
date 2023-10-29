from get_information_for_company import Get_info_stock







symboles = ['MSFT','ZION','IBM','JNJ','MCD']
def main():
    # call the extract function
    #extract_ticker()
    # call the transform function
    get_all = Get_info_stock(symboles)
    get_all.transform_data()
    # call the load function
    get_all.load_mongo()
    return True

### Run Layer ###

if __name__ == '__main__':
    main()
    print('Data has been extracted, transformed, saved in a json file and loaded into mongodb')