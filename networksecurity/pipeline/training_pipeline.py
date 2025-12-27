## will be almost same as our main.py

import os
import sys

from networksecurity.logging.logger import logging
from networksecurity.execption.exception import CustomException

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer


from networksecurity.entity.config_entity import (DataIngestionConfig,
                                                  TrainingPipelineConfig,
                                                  DataValidationConfig,
                                                  ModelTrainerConfig,
                                                  DataTransformationConfig
                                                  )
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)
from networksecurity.constants.training_pipeline import TRANING_BUCKET_NAME
from networksecurity.cloud.s3_syncer import S3Sync


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()
        self.s3_sync=S3Sync()
        
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Started data ingestion")
            training_pipeline_config=self.training_pipeline_config
            self.data_ingestion_config=DataIngestionConfig(training_pipeline_config)
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("Data ingestion completed and artifact: %s",data_ingestion_artifact)
            return data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            logging.info("Starting data validation")
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_validation_config,data_ingestion_artifact)
            data_validation_artifact=data_validation.initiate_data_validation()
            
            logging.info("data validation completed and artifact: %s",data_validation_artifact)
            return data_validation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_transformation(self,data_validation_artifact)->DataTransformationArtifact:
        try:
            logging.info("Starting data transformation")
            data_transformation_config=DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_tranformation=DataTransformation(
                data_transformation_config=data_transformation_config,
                data_validation_artifact=data_validation_artifact
            )
            data_transformation_artifact=data_tranformation.inititate_data_tranformation()
            logging.info("Data transforrmation completed")
            
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_model_training(self,data_transformation_artifact)->ModelTrainerArtifact:
        try:
            logging.info("Starting model training")
            self.model_trainer_config=ModelTrainerConfig(self.training_pipeline_config)
            model_trainer=ModelTrainer(
                model_trainer_config=self.model_trainer_config,
                data_tranformation_artifact=data_transformation_artifact
                )
            model_trainer_artifact=model_trainer.initiate_model_trainer()
            logging.info("Model training Completed")
            
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    def sync_artifact_to_s3(self):
        try:
            aws_bucket_url=f"s3://{TRANING_BUCKET_NAME}/artifact/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.artifact_dir,
                                           aws_bucket_url=aws_bucket_url
                                           )
        except Exception as e:
            raise CustomException(e,sys)
    
    def sync_saved_model_dir_to_s3(self):
        try:
            aws_bucket_url=f"s3://{TRANING_BUCKET_NAME}/final_model/{self.training_pipeline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder=self.training_pipeline_config.model_dir,
                                           aws_bucket_url=aws_bucket_url
                                           )
        except Exception as e:
            raise CustomException(e,sys)
        
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
            
            model_trainer_artifact=self.start_model_training(data_transformation_artifact)
            
            self.sync_artifact_to_s3()
            self.sync_saved_model_dir_to_s3()
            
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)
    