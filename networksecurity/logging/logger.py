import logging 
import os
from datetime import datetime

LOGS_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
# 2025-01-12 23:45:10.log

logs_path=os.path.join(os.getcwd(),"logs",LOGS_FILE)
#cwd/logs/2025-01-12 23:45:10.log

os.makedirs(logs_path,exist_ok=True)

LOG_FILE_PATH=os.path.join(logs_path,LOGS_FILE)


logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    
)


# if __name__=="__main__":
#     logging.info("logging works")