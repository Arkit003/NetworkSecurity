import os
import sys
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp


from networksecurity.execption.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataIngestionArtifact
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file

class DataValidation:
    def __init__(self,data_validation_config:DataValidationConfig,
                 data_ingestion_artifact:DataIngestionArtifact
                 ):
        try:
            self.data_validation_config=data_validation_config
            self.data_ingestion_artifact=data_ingestion_artifact
            self.schema_config=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise CustomException(e,sys)
        
    def read_data(self,train_file_path,test_file_path):
        try:
            train_df=pd.read_csv(train_file_path)
            test_df=pd.read_csv(test_file_path)
            
            return train_df,test_df
        
        except Exception as e:
               raise CustomException(e,sys) 
           
    def validating_columns(self,train_df,test_df):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
    
    def initiate_data_validation(self):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)