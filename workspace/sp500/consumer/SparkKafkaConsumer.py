

from datetime import datetime



from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json 


class BaseKafkaConsumer():
    """
    Base class for Kafka streaming consumers using Spark.
    """

    def __init__(self,bucket, kafka_bootstrap_servers, topic,schema,formats,storage_access:dict):
        """
        Set Kafka and output path configuration.
        """

        self.topic = topic  
        self.schema = schema
        self.bucket = bucket      
        self.kafka_bootstrap_servers = kafka_bootstrap_servers
        self.formats = formats
        self.storage_access=storage_access
        self.spark = self._create_spark_session()

    def _create_spark_session(self):
        """
        Create Spark session configured for AWS S3.
        """
        spark = SparkSession.builder\
            .appName("KafkaToS3")\
            .master("local[*]")\
            .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0,org.apache.hadoop:hadoop-aws:3.3.1")\
            .config("spark.hadoop.fs.s3a.access.key", self.storage_access['access_key'])\
            .config("spark.hadoop.fs.s3a.secret.key", self.storage_access['secret_key'])\
            .config("spark.hadoop.fs.s3a.endpoint", self.storage_access['endpoint'])\
            .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")\
            .config("spark.hadoop.fs.s3a.path.style.access", "true")\
            .config("spark.driver.extraJavaOptions", "-Dlog4j.configuration=file:/project/log4j.properties")\
            .getOrCreate()
    
        spark.sparkContext.setLogLevel("ERROR")
        return spark
    def _parse_kafka_stream(self):
        """
        Read and parse Kafka stream into a structured DataFrame.
        """
        raw_df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.kafka_bootstrap_servers) \
            .option("subscribe", self.topic) \
            .option("startingOffsets", "earliest") \
            .load()

        parsed_df = raw_df.selectExpr("CAST(value AS STRING)") \
            .select(from_json(col("value"), self.schema).alias("data")) \
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

    def _write_batch_to_s3(self, batch_df, batch_id):
        """
        Write a batch to datalake in JSON , Parquet or other formats.
        """
        if batch_df is None or batch_df.rdd.isEmpty():
            print(f"⚠️ Batch {batch_id} is empty — skipping.")
            return


        now = datetime.utcnow()
        timestamp = now.strftime("%Y-%m-%dT%H-%M-%S")
        date_path = now.strftime("%Y/%m/%d/%H")

        for fmt in self.formats:
            path = f"s3a://{self.bucket}/{fmt}/{date_path}/batch_{timestamp}"

            try:
                batch_df.write.mode("append").format(fmt).save(path)
                print(f"✅ {fmt.upper()} written to: {path}")
            except Exception as e:
                print(f"❌ Failed to write {fmt} for batch {batch_id}: {e}")