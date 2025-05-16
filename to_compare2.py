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