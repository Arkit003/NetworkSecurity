#this file gona extract the data from the csv and push to mongodb

import os
import sys
import json
import pandas as pd
import numpy as np
import pymongo

from dotenv import load_dotenv

from networksecurity.logging.logger import logging
from networksecurity.execption.exception import CustomException



load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")




import certifi## creates ceritficates that helps in making http connection,like here with mongo db

ca=certifi.where()#gives the file path where certificates are


class NetworkDataExtract:
    def __init__(self):
        pass
        
    def csv_to_json(self,file_path):
        
        '''
        loading the csv and converting it into df and converting into apporopritate
        format to upload to mongo db
        {
            "0": {"col1": 10, "col2": "abc"},
            "1": {"col1": 20, "col2": "def"}
        }
        
        Returns:records->in mondodb format
        '''
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)#drropping the first column as it creates a column for the first line of csv when reading it             
            # records=list(json.loads(data.T.to_json()).values())
            # #data.T.to_json()-transpose the dataframe
            # #Converts it to JSON like:
            # # {
            # #   "0": {"col1": 10, "col2": "abc"},
            # #   "1": {"col1": 20, "col2": "def"}
            # # }
            # #json.loads- converts json to dict
            # #.values() -extracts the inner dict
            # #[{"col1":10,"col2":"abc"}, {"col1":20,"col2":"def"}]
            
            #a better way to do the same
            records = data.to_dict(orient="records")
            return records
            
        except Exception as e:
            raise CustomException(e,sys)        
        
    def push_to_mongodb(self,records,database,collection):
        try:
            self.database=database
            self.collection=collection
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_client[database]
            self.collection=self.database[collection]
            
            self.collection.insert_many(records)
            
            return (len(records))
        
        except Exception as e:
            raise CustomException(e,sys)
            
            
#executing the ETL pipelline

if __name__=="__main__":
    network_data_extract=NetworkDataExtract()
    CSV_PATH="network_data/phisingData.csv"
    DATABASE="ArkitAi"
    COLLECTION="NetworkData"
    records=network_data_extract.csv_to_json(CSV_PATH)
    
    no_of_records=network_data_extract.push_to_mongodb(records,DATABASE,COLLECTION)
    print(records)
    print(no_of_records)
    
    