
import sys

from networksecurity.execption.exception import CustomException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME


class NetworkModel:
    '''
    scaling and prdicting output for the new data
    
    Args:model,preprocessor
    
    Return:y_hat:model predicted output
    '''
    
    def __init__(self,model,preprocessor):

        try:
            self.model=model
            self.preprocessor=preprocessor
        except Exception as e:
            raise CustomException(e,sys)
        
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transform)
            
            return y_hat
        
        except Exception as e:
            raise CustomException(e,sys)