import os
import sys
import pandas as pd
import numpy as np
import mlflow
import dagshub

from dotenv import load_dotenv
load_dotenv()



from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier
)


from networksecurity.utils.main_utils.utils import load_numpy_array_data,evaluate_model
from networksecurity.utils.main_utils.utils import save_object,load_object
from networksecurity.utils.ml_utils.metrics.classification_metric import get_classfication_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel

from networksecurity.execption.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,ClassificationonMetricArtifact,DataTransformationArtifact

#dagshub initilization
os.environ["DAGSHUB_USER_TOKEN"]=os.getenv("DAGSHUB_USER_TOKEN")
dagshub.init(repo_owner='Arkit003', repo_name='NetworkSecurity', mlflow=True)
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
        
    def track_mlflow(self,best_model,classifactionmetric):
        try:
            with mlflow.start_run():
                f1_score=classifactionmetric.f1_score
                precision_score=classifactionmetric.precision_score
                recall_score=classifactionmetric.recall_score
                
                mlflow.log_metric("f1 score",f1_score)
                mlflow.log_metric("precision_score",precision_score)
                mlflow.log_metric("recall_score",recall_score)
                ##loggging our model also
                mlflow.sklearn.log_model(best_model,"model")
                
        except Exception as e:
            raise CustomException(e,sys)
        
    def train_model(self,x_train,y_train,x_test,y_test):
        
        '''
        performing modelselection,hyperparmetertuning ,scaling and predicting the output
        
        Return: ModelTrainerArtifact
        
        '''
        try:
            models={
                "Random Forest":RandomForestClassifier(verbose=1),
                "Decision Tree":DecisionTreeClassifier(),
                "Gradient Boosting":GradientBoostingClassifier(verbose=1),
                "Logistic Regression":LogisticRegression(verbose=1),
                "AdaBoost":AdaBoostClassifier(),
            }
            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,64,128,256]
            }
            
            }
            model_report:dict =evaluate_model(x_train,y_train,x_test,y_test,models,params)
            
            best_model_score=max(sorted(model_report.values()))
            
            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model=models[best_model_name]
            y_train_pred=best_model.predict(x_train)
            
            classification_train_metric=get_classfication_score(y_true=y_train,y_pred=y_train_pred)
            
            ## tracking with ml flow
            #help in tracking which model is performing best
            self.track_mlflow(best_model,classification_train_metric)
            
            y_test_pred=best_model.predict(x_test)
            classification_test_metric= get_classfication_score(y_true=y_test,y_pred=y_test_pred)
            self.track_mlflow(best_model,classification_test_metric)
            
            
            preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)
            
            model_dir_path=os.path.dirname(self.model_trainer_config.trained_model_file_path)
            os.makedirs(model_dir_path,exist_ok=True)
            
            ## we can save preprocess and model and prediction pipline in a pkl file with save object
            ## pickle can save it 
            Network_Model=NetworkModel(preprocessor=preprocessor,model=best_model)
            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=Network_Model
                )
            
            ## creating  the modeltrainerartifact to return
            model_trainer_arifact=ModelTrainerArtifact(
                trained_model_file_path=self.model_trainer_config.trained_model_file_path,
                train_metric_artifact=classification_train_metric,
                test_metric_artifact=classification_test_metric
            )
            
            logging.info(f"model trainer artifact: {model_trainer_arifact}")
            
            #saving our models and preprocessor for best models
            #cuz of more models our model size could be very much
            #so we will gonna store it into cloud instead of local or github
            #in aws EC2 instance
            save_object("final_model/model.pkl",best_model)
            
            
            return model_trainer_arifact
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_arr_file_path=self.data_transformation_artifact.transformed_train_file_path
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
            
            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            
            return model_trainer_artifact
            
        except Exception as e:
            raise CustomException(e,sys)
        
        