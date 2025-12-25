import yaml
import os,sys
import numpy as np
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


from networksecurity.execption.exception import CustomException
from networksecurity.logging.logger import logging

def read_yaml_file(file_path:str) -> dict:
    try:
        with open(file_path,'rb') as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise CustomException(e,sys)
    
def write_yaml_file(file_path:str,content : object,replace:bool=False )->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
                
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as yaml_file:
            yaml.dump(content,yaml_file)
    except Exception as e:
        raise CustomException(e,sys)
    
def save_numpy_array_data(file_path:str ,array:np.array)->None:
    '''
    Save numpy data to file
    '''
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
            
    except Exception as e:
        raise CustomException(e,sys)
    
def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,'rb') as file_obj:
            return np.load(file_obj) 
    except Exception as e:
        raise CustomException(e,sys)
    
def save_object(file_path:str,obj:object)->None:
    '''
    saving object file such as pickle(.pkl)
    '''
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            pickle.dump(obj,file_obj)
    except Exception as e:
        raise CustomException(e,sys)
    

def load_object(file_path:str)->object:
    try:
        if not os.path.exists(file_path):
            raise Exception (F"the file: {file_path} does not exist")
        with open(file_path,'rb') as file_obj:
            obj=pickle.load(file_obj)
            
        return obj
    
    except Exception as e:
        raise CustomException(e,sys)
    
    
def evaluate_model(x_train,y_train,x_test,y_test,models,params):
    try:
        report={}
        
        for i in range(len(models)):
            model=list(models.values())[i]
            param=params[list(models.keys())[i]]
            
            gs=GridSearchCV(estimator=model,param_grid=param,cv=3)
            gs.fit(x_train,y_train)
            
            model.set_params(**gs.best_params_)
            model.fit(x_train,y_train)
            
            y_train_pred=model.predict(x_train)
            
            y_test_pred=model.predict(x_test)
            
            train_model_score=r2_score(y_train,y_train_pred)
            
            test_model_score=r2_score(y_test,y_test_pred)
            
            report[list(models.keys())[i]]=test_model_score
            
        return report
            
    except Exception as e:
        raise CustomException(e,sys)