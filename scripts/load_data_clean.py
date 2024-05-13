import pandas as pd
import re
from datetime import datetime, timedelta
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def main():
    uri = "mongodb+srv://wahpram2607:Bangli123.@cluster0.yiobiyk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    path = './data/data_tanah_bali_clean.csv'
    db_name = 'data_tanah_bali'
    collection_name = 'list_tanah_bali_clean'
    
    data = pd.read_csv(path)
    
    try:
        client = MongoClient(uri, server_api=ServerApi('1'))
        
        print('---------------------------------------')
        print('Connected to db')
        data_to_insert = data.to_dict('records')
        
        db = client[db_name]
        collection = db[collection_name]
        
        collection.insert_many(data_to_insert)
        coll_len = collection.count_documents({})
        
        print(f'Total documents: {coll_len}')
        
        client.close()
        
    except Exception as e:
        print(e)
        
        
if __name__ == '__main__':
    main()