import os
import sys




'''
Defiing common constants
'''

TARGET_COLUMN="Result"
FILE_NAME:str='phisingData.csv'
PIPELINE_NAME:str="NetworkSecurity"
ARTIFACT_DIR:str="artifact"

TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

'''
Data ingestion related components
'''

DATA_INGESTION_COLLECTION_NAME:str="NetworkData"
DATA_INGESTION_DATABASE_NAME:str="ArkitAi"
DATA_INGESTION_DIR_NAME:str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR:str='feature_store'
DATA_INGESTION_INGESTED_DIR:str="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO:float= 0.2