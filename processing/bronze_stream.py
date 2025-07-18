# processing/bronze_stream.py

from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# 1) Build your SparkSession
spark = (
    SparkSession.builder
    .appName("bronze_kafka_ingest")
    .getOrCreate()
)

# 2) Define your JSON schema
schema = StructType([
    StructField("event_time", TimestampType()),
    StructField("user_id", StringType()),
    StructField("action", StringType()),
    StructField("value", StringType()),
])

# 3) Read the stream from Kafka
df = (
    spark.readStream
      .format("kafka")
      .option("kafka.bootstrap.servers", "kafka:9092")
      .option("subscribe", "topic-name")
      .option("startingOffsets", "latest")
      .load()
)

# 4) Parse and select
parsed = (
    df.select(from_json(col("value").cast("string"), schema).alias("data"))
      .select("data.*")
)

# 5) Write to Bronze Iceberg table on MinIO
(
    parsed.writeStream
          .format("iceberg")
          .option("path", "s3a://bucket-bronze/iceberg/bronze_table")
          .option("checkpointLocation", "/tmp/checkpoints/bronze")
          .outputMode("append")
          .start()
          .awaitTermination()
)
