
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
AWS_S3_BUCKET = "final-de-project-sp500"


#############MINIO#######################
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin"
MINIO_ENDPOINT = "http://minio:9000"
MINIO_BUCKET = "final-de-project-sp500"