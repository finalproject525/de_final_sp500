try:
    #when run in consumer container
    from SparkKafkaConsumer import SparkKafkaConsumer
except ImportError:
    #when runing from dev container
    from consumer.SparkKafkaConsumer import SparkKafkaConsumer
    
from config import AWS_S3_BUCKET, BROKER, TOPIC


def main():
    consumer = SparkKafkaConsumer(
        kafka_bootstrap_servers=BROKER[0],
        topic=TOPIC,
        s3_bucket=AWS_S3_BUCKET,
        json_prefix="json",
        parquet_prefix="parquet"
    )
    consumer.start()

if __name__ == "__main__":
    main()

