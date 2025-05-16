
import os
from abc import ABC, abstractmethod
from datetime import datetime



from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType

from config import MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_ENDPOINT


class BaseKafkaConsumer(ABC):
    """
    Base class for Kafka streaming consumers using Spark.
    """

    def __init__(self, kafka_bootstrap_servers, topic, json_prefix, parquet_prefix):
        """
        Set Kafka and output path configuration.
        """
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.topic = topic
        self.json_prefix = json_prefix
        self.parquet_prefix = parquet_prefix
        self.spark = self._create_spark_session()

    @abstractmethod
    def _create_spark_session(self):
        """
        Must return a configured SparkSession.
        """
        raise NotImplementedError("Subclasses must implement _create_spark_session")

    @abstractmethod
    def _write_batch_to_s3(self, batch_df, batch_id):
        """
        Must define how to write a batch to S3 or MinIO.
        """
        raise NotImplementedError("Subclasses must implement _write_batch_to_s3")

    def _parse_kafka_stream(self):
        """
        Read and parse Kafka stream into a structured DataFrame.
        """
        schema = StructType() \
            .add("Open", StringType()) \
            .add("High", StringType()) \
            .add("Low", StringType()) \
            .add("Close", StringType()) \
            .add("Volume", StringType()) \
            .add("symbol", StringType()) \
            .add("timestamp", StringType()) \
            .add("datetime", StringType())

        raw_df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("subscribe", self.topic) \
            .option("startingOffsets", "earliest") \
            .load()

        parsed_df = raw_df.selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), schema).alias("data")) \
            .select("data.*")

        return parsed_df

    def start(self):
        """
        Start the Spark streaming job.
        """
        df = self._parse_kafka_stream()

        query = df.writeStream \
            .foreachBatch(self._write_batch_to_s3) \
            .outputMode("append") \
            .start()

        query.awaitTermination()


class S3KafkaConsumer(BaseKafkaConsumer):
    """
    Kafka consumer that writes data to AWS S3 using Spark.
    """

    def __init__(self, kafka_bootstrap_servers, topic, s3_bucket, json_prefix, parquet_prefix):
        """
        Initialize with S3 bucket and output prefixes.
        """
        self.s3_bucket = s3_bucket
        super().__init__(kafka_bootstrap_servers, topic, json_prefix, parquet_prefix)

    def _create_spark_session(self):
        """
        Create Spark session configured for AWS S3.
        """
        return (
            SparkSession.builder
            .appName("KafkaToS3")
            .master("local[*]")
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.hadoop:hadoop-aws:3.3.1")
            .config("spark.hadoop.fs.s3a.access.key", os.getenv("AWS_ACCESS_KEY_ID"))
            .config("spark.hadoop.fs.s3a.secret.key", os.getenv("AWS_SECRET_ACCESS_KEY"))
            .config("spark.hadoop.fs.s3a.endpoint", f"s3.{os.getenv('AWS_DEFAULT_REGION')}.amazonaws.com")
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .getOrCreate()
        )

    def _write_batch_to_s3(self, batch_df, batch_id):
        """
        Write a batch to S3 in JSON and Parquet formats.
        """
        if batch_df.rdd.isEmpty():
            print(f"⚠️ Batch {batch_id} is empty — skipping.")
            return

        now = datetime.utcnow()
        timestamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        date_path = now.strftime("%Y/%m/%d/%H")

        json_path = f"s3a://{self.s3_bucket}/{self.json_prefix}/{date_path}/batch_{timestamp}.json"
        parquet_path = f"s3a://{self.s3_bucket}/{self.parquet_prefix}/{date_path}/batch_{timestamp}.parquet"

        try:
            batch_df.write.mode("append").json(json_path)
            print(f"✅ JSON written to: {json_path}")

            batch_df.write.mode("append").parquet(parquet_path)
            print(f"✅ Parquet written to: {parquet_path}")
        except Exception as e:
            print(f"❌ Failed to write batch {batch_id}: {e}")

 
class MinIOKafkaConsumer(BaseKafkaConsumer):
    """
    Kafka consumer that writes data to MinIO using Spark.
    """

    def __init__(self, kafka_bootstrap_servers, topic, minio_bucket, json_prefix, parquet_prefix):
        """
        Initialize with MinIO bucket and output prefixes.
        """
        self.minio_bucket = minio_bucket
        super().__init__(kafka_bootstrap_servers, topic, json_prefix, parquet_prefix)

    def _create_spark_session(self):
        """
        Create Spark session configured for MinIO.
        """
        return (
            SparkSession.builder
            .appName("KafkaToMinIO")
            .master("local[*]")
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.hadoop:hadoop-aws:3.3.1")
            .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY)
            .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY)
            .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT)
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
            .config("spark.hadoop.fs.s3a.path.style.access", "true")
            .getOrCreate()
        )

    def _write_batch_to_s3(self, batch_df, batch_id):
        """
        Write a batch to MinIO in JSON and Parquet formats.
        """
        if batch_df.rdd.isEmpty():
            print(f"⚠️ Batch {batch_id} is empty — skipping.")
            return

        now = datetime.utcnow()
        timestamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        date_path = now.strftime("%Y/%m/%d/%H")

        json_path = f"s3a://{self.minio_bucket}/{self.json_prefix}/{date_path}/batch_{timestamp}.json"
        parquet_path = f"s3a://{self.minio_bucket}/{self.parquet_prefix}/{date_path}/batch_{timestamp}.parquet"

        try:
            batch_df.write.mode("append").json(json_path)
            print(f"✅ JSON written to: {json_path}")

            batch_df.write.mode("append").parquet(parquet_path)
            print(f"✅ Parquet written to: {parquet_path}")
        except Exception as e:
            print(f"❌ Failed to write batch {batch_id}: {e}")
