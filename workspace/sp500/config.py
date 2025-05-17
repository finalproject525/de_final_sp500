import os
#######################TEST VARIABLES##########################

""" change to False to send data to AWS S3 """
USE_MINIO = True

"change to True to get all 500 Tickers of sp500"
USE_SYMBOLES_TEST = False
SYMBOLS_TEST = ["AAPL", "MSFT", "GOOG","TSLA","NVDA","META","AMZN"]





################ yfinance api config#############################
PERIOD = "1d"
INTERVAL = "60m" 
API_BATCH_SIZE = 50

################ Kafka Config ###################################
TOPIC = 'yfinance-data'
BROKER = ['kafka_alt:9092']
BATCH_SIZE = 100
USE_DYNAMIC_GROUP = False

################### AWS #########################################

OUTPUT_FORMATS = ['json', 'parquet']
S3_ACCESS= {'access_key':os.getenv("AWS_ACCESS_KEY_ID"),
            'secret_key':os.getenv("AWS_SECRET_ACCESS_KEY"),
            'endpoint':f"s3.{os.getenv('AWS_DEFAULT_REGION')}.amazonaws.com"
        }
BUCKET = "final-de-project-sp500" 

#############MINIO#######################

MINIO_ACCESS= {'access_key':'minioadmin',
               'secret_key':'minioadmin',
               'endpoint':'http://minio:9000'
               }


