import logging

logging.basicConfig(  
    level=logging.DEBUG,  
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  
    handlers=[  
        logging.FileHandler("app.log"),  
        logging.StreamHandler()  
    ]  
)  
  