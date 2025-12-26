import os,sys
import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.logging.logger import logging
from networksecurity.execption.exception import CustomException
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.entity.artifact_entity import DataTransformationArtifact,DataValidationArtifact
from networksecurity.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        try:
            self.data_transformation_config=data_transformation_config
            self.data_validation_artifact=data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)

    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_data_transformer_object(cls)->Pipeline:
        '''
        Returns: A Pipeline object
        '''
        
        logging.info("Entering get data transformation funstion of data transformation class")
        try:
            imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            
            preprocessor:Pipeline=Pipeline([("imputer",imputer)])
            
            return preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def inititate_data_tranformation(self)->DataTransformationArtifact:
        logging.info("Entering the initiation of data transformation pipeline")
        try:
            ## this data already contain values from just -1to1 
            ## so we dont standard scaled the data
            logging.info("reading the train and test files ")
            train_df__file_path=self.data_validation_artifact.valid_train_file_path
            test_df__file_path=self.data_validation_artifact.valid_test_file_path
            train_df=DataTransformation.read_data(file_path=train_df__file_path)
            test_df=DataTransformation.read_data(file_path=test_df__file_path)
            logging.info("reading done")
            
            logging.info("creating the  input and result feature dataframes")
            input_feature_train_df=train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df=train_df[TARGET_COLUMN]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            
            input_feature_test_df=test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df=test_df[TARGET_COLUMN] 
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            
            preprocessor=self.get_data_transformer_object()
            
            preprocessor_object=preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature=preprocessor.transform(input_feature_train_df)
            transformed_input_test_feature=preprocessor.transform(input_feature_test_df)
            
            #concating  the columns to form one array of all features
            #c_ in short stands for np.concatinate
            train_arr=np.c_[
                transformed_input_train_feature,np.array(target_feature_train_df)
            ]
            test_arr=np.c_[
                transformed_input_test_feature,np.array(target_feature_test_df)
            ]
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path,train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path,test_arr)
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)
            
            ## saving for final model
            save_object("final_models/preprocessor.pkl",preprocessor_object)
            
            data_transformation_artifact=DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            )
            logging.info("data transformation done")
            
            
            return data_transformation_artifact
            
            
        except Exception as e:
            raise CustomException(e,sys)