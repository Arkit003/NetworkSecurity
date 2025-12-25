#for testing purposes

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
                                                  ModelTrainerConfig
                                                  )
from networksecurity.entity.config_entity import DataTransformationConfig

if __name__=="__main__":
    try:
        training_pipeline_config=TrainingPipelineConfig()
        data_ingestion_config=DataIngestionConfig(training_pipeline_config)
        data_ingestion=DataIngestion(data_ingestion_config=data_ingestion_config)

        logging.info("inititating the dataingestion")
        data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
        # print(data_ingestion_artifact)#we could print this as @dataclass has a __repr function
        logging.info("Data ingestion completed")
        
        logging.info("Starting data validation")
        data_validation_config=DataValidationConfig(training_pipeline_config=training_pipeline_config)
        data_validation=DataValidation(data_validation_config,data_ingestion_artifact)
        data_validation_artifact=data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("data validation completed")
        
        logging.info("Starting data transformation")
        
        data_transformation_config=DataTransformationConfig(training_pipeline_config=training_pipeline_config)
        data_tranformation=DataTransformation(
            data_transformation_config=data_transformation_config,
            data_validation_artifact=data_validation_artifact
        )
        data_transformation_artifact=data_tranformation.inititate_data_tranformation()
        print(data_transformation_artifact)
        logging.info("Data transforrmation completed")
        
        
        logging.info("Starting model training")
        model_trainer_config=ModelTrainerConfig(training_pipeline_config)
        model_trainer=ModelTrainer(
            model_trainer_config=model_trainer_config,
            data_tranformation_artifact=data_transformation_artifact
            )
        model_trainer_artifact=model_trainer.initiate_model_trainer()
        print(model_trainer_artifact)
        
        logging.info("Model training Completed")
    except Exception as e:
        raise CustomException(e,sys)