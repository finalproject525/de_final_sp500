try:
    #when run in consumer container
    from SparkKafkaConsumer import BaseKafkaConsumer
except ImportError:
    #when runing from dev container
    from consumer.SparkKafkaConsumer  import BaseKafkaConsumer
    
from config import USE_MINIO,BROKER,TOPIC,BUCKET,OUTPUT_FORMATS,MINIO_ACCESS,S3_ACCESS
from config import OUTPUT_FORMATS
from schemas.schemas import schema_yfinance

def main():

    STORAGE_ACCESS = MINIO_ACCESS if USE_MINIO else S3_ACCESS


    consumer = BaseKafkaConsumer(
        
            bucket=BUCKET,
            kafka_bootstrap_servers=BROKER[0],
            topic=TOPIC,
            schema=schema_yfinance,
            formats=OUTPUT_FORMATS,
            storage_access = STORAGE_ACCESS
    )

    consumer.start()

if __name__ == "__main__":
    main()