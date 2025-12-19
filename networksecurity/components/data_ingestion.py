import os
import sys
import pymongo
import pandas as pd
import numpy as np

from dotenv import load_dotenv
from sklearn.model_selection import train_test_split



from networksecurity.execption.exception import CustomException
from networksecurity.logging.logger import logging

#adding data ingestion config
from networksecurity.entity.config_entity import DataIngestionConfig,TrainingPipelineConfig

load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_ingestion(self):
        
        logging.info("Entered the data ingestion method or component")
        
        try:
            df=pd.read_csv("network_data/phisingData.csv")
            logging.info("the dataset has been read")
            
            os.makedirs(os.path.dirname())
        except Exception as e:
            raise CustomException(e,sys)
