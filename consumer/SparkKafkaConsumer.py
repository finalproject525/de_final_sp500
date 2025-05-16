import json
from pyspark.sql import SparkSession

from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StringType

from config import USE_DYNAMIC_GROUP

try :
    from services.aws.S3Uploader import S3Uploader
except ImportError:
        #when runing from dev container
    from services.aws.S3Uploader import S3Uploader


class SparkKafkaConsumer:
    def __init__(self, kafka_bootstrap_servers, topic, s3_bucket, json_prefix="json", parquet_prefix="parquet"):
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.topic = topic
        self.s3_bucket = s3_bucket
        self.json_prefix = json_prefix
        self.parquet_prefix = parquet_prefix
        self.spark = self._create_spark_session()
        self.uploader = S3Uploader(bucket_name=self.s3_bucket)

    def _create_spark_session(self):
        spark = SparkSession.builder \
            .appName("KafkaSparkToS3") \
            .master("local[*]") \
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0") \
            .getOrCreate()
        spark.sparkContext.setLogLevel("ERROR")
        return spark
    def _parse_kafka_stream(self):
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
    def _write_batch_to_s3(self, batch_df, batch_id):
        # Check if the batch is empty
        if batch_df.rdd.isEmpty():
            print(f"⚠️ Batch {batch_id} is empty — skipping S3 upload.")
            return

        # Count the number of rows in the batch
        row_count = batch_df.count()
        print(f"📊 Batch {batch_id} has {row_count} rows.")

        try:
            # Convert the Spark DataFrame to a list of Python dictionaries
            records = batch_df.toJSON().map(lambda x: json.loads(x)).collect()

            print(f"📤 Uploading batch {batch_id} to S3...")

            # Upload JSON to S3
            self.uploader.upload_json(records, prefix=self.json_prefix)

            # Upload Parquet to S3
            self.uploader.upload_as_parquet(records, prefix=self.parquet_prefix)

        except Exception as e:
            print(f"❌ Failed to process or upload batch {batch_id}: {e}")




    def _make_parquet_key(self, batch_id):
        return f"{self.parquet_prefix}/batch_{batch_id}.parquet"

    def start(self):
        df = self._parse_kafka_stream()

        query = df.writeStream \
            .foreachBatch(self._write_batch_to_s3) \
            .outputMode("append") \
            .start()

        query.awaitTermination()
