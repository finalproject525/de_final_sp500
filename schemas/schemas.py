from pyspark.sql.types import StructType, StringType

schema_yfinance = StructType() \
    .add("Open", StringType()) \
    .add("High", StringType()) \
    .add("Low", StringType()) \
    .add("Close", StringType()) \
    .add("Volume", StringType()) \
    .add("symbol", StringType()) \
    .add("timestamp", StringType()) \
    .add("datetime", StringType())


schema_finnhub = StructType() \
    .add("price", StringType()) \
    .add("ticker", StringType()) \
    .add("ts", StringType())