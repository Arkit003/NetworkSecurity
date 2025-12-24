import os
import sys
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split

from networksecurity.utils.main_utils.utils import load_numpy_array_data
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.ml_utils.metrics.classification_metric import get_classfication_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.execption.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,ClassificationonMetricArtifact,DataTransformationArtifact

class ModelTrainer:
    def __init__(
        self,
        model_trainer_config:ModelTrainerConfig,
        data_tranformation_artifact:DataTransformationArtifact
        
                 ):
        try:
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_tranformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def train_model(self,x_train,y_train):
        try:
            pass
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_arr_file_path=self.data_transformation_artifact.transformed_test_file_path
            test_arr_file_path=self.data_transformation_artifact.transformed_test_file_path
            train_arr=load_numpy_array_data(train_arr_file_path)
            test_arr=load_numpy_array_data(test_arr_file_path)
            
            #dont need to use train test test split as we have already done that 
            x_train,y_train,x_test,y_test=(
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )
            
            model=self.train(x_train,y_train)
            
        except Exception as e:
            raise CustomException(e,sys)
        
        