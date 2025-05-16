import os
import json
import boto3 
from io import BytesIO
from pyarrow import Table
import pyarrow.parquet as pq
from datetime import datetime 
from botocore.exceptions import BotoCoreError, ClientError

class S3Uploader:
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_DEFAULT_REGION')
        )

    def upload_json(self, data: list[dict], prefix: str = "kafka"):
        try:
            now = datetime.utcnow()
            timestamp = now.strftime("%Y-%m-%dT%H-%M-%S")
            date_path = now.strftime("%Y/%m/%d/%H")

            # Full key with date structure
            key = f"{prefix}/{date_path}/data_{timestamp}.json"
            content = json.dumps(data, indent=2)

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=content
            )
            print(f"✅ JSON upload successful: s3://{self.bucket_name}/{key}")
        except (BotoCoreError, ClientError) as e:
            print(f"❌ JSON upload failed: {e}")
            raise

    def upload_as_parquet(self, data: list[dict], prefix: str = "kafka"):
        try:
            now = datetime.utcnow()
            timestamp = now.strftime("%Y-%m-%dT%H-%M-%S")
            date_path = now.strftime("%Y/%m/%d/%H")

            key = f"{prefix}/{date_path}/data_{timestamp}.parquet"

            # Convert to Arrow table
            table = Table.from_pylist(data)
            buffer = BytesIO()
            pq.write_table(table, buffer)
            buffer.seek(0)

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=buffer.getvalue()
            )

            print(f"✅ Parquet upload successful: s3://{self.bucket_name}/{key}")

        except (BotoCoreError, ClientError, Exception) as e:
            print(f"❌ Parquet upload failed: {e}")
            raise

