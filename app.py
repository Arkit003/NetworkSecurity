import os
import sys

import certifi
from dotenv import load_dotenv
import pymongo
import pandas as pd

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI,File,UploadFile,Request
from uvicorn import run as app_run
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates


from networksecurity.execption.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.main_utils.utils import load_object
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.constants.training_pipeline import DATA_INGESTION_DATABASE_NAME,DATA_INGESTION_COLLECTION_NAME


load_dotenv()

ca=certifi.where()
mongo_db_url=os.getenv("MONGO_DB_URL")
client=pymongo.MongoClient(mongo_db_url,tlsCAFile=ca)
database=client[DATA_INGESTION_DATABASE_NAME]
collection=client[DATA_INGESTION_COLLECTION_NAME]

app=FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates=Jinja2Templates(directory="./templates")

@app.get("/",tags=["authentication"])
async def index():
    return RedirectResponse("/docs")

@app.get("/train")
async def train_route():
    '''
    will gonna start the training in the cli or the cloud 
    '''
    
    try:
        train_pipeline=TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training is successful")
    
    except Exception as e:
        raise CustomException(e,sys)
    
@app.post("/predict")
async def predict_route(request:Request,file:UploadFile=File(...)):
    try:
        df=pd.read_csv(file.file)
        
        model=load_object("final_model/model.pkl")
        preprocessor=load_object("final_model/preprocessor.pkl")
        network_model=NetworkModel(model=model,preprocessor=preprocessor)
        
        y_pred=network_model.predict(df)
        df['Predicted Outcome']=y_pred

        os.makedirs("prediction_data", exist_ok=True)
        df.to_csv("prediction_data/predicted.csv")
        
        table_html=df.to_html(classes='table table-striped')
        
        return templates.TemplateResponse("table.html",{"request":request,"table":table_html})
        
    except Exception as e:
        raise CustomException(e,sys)
            

if __name__=="__main__":
    app_run(app,host="localhost",port=8000)

