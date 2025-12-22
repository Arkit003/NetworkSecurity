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
from networksecurity.entity.artifact_entity import DataTranformationArtifact,DataValidationArtifact
from networksecurity.constants.training_pipeline import TARGET_COLUMN,DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_transformation_config:DataTransformationConfig,data_validation_artifact:DataValidationArtifact):
        self.data_transformation_config=data_transformation_config
        self.data_validation_artifact=data_validation_artifact

    @staticmethod
    def read_data(file_path:str)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e,sys)
        
    def inititate_data_tranformation(self)->DataTranformationArtifact:
        try:
            train_df__file_path=self.data_validation_artifact.valid_train_file_path
            test_df__file_path=self.data_validation_artifact.valid_test_file_path
            train_df=DataTransformation.read_data(file_path=train_df__file_path)
            test_df=DataTransformation.read_data(file_path=test_df__file_path)
            
            target_train_df=train_df[::-1]
        except Exception as e:
            raise CustomException(e,sys)