from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

# הגדרת SparkSession
spark = SparkSession.builder \
    .appName("bronze_to_silver_stream") \
    .getOrCreate()

# הגדרת סכמת JSON
schema = StructType([
    StructField("event_time", TimestampType()),
    StructField("user_id", StringType()),
    StructField("action", StringType()),
    StructField("value", StringType())
])

# קריאה ל‑Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "your-topic") \
    .load()

# המרת נתונים
parsed_df = df.select(from_json(col("value").cast("string"), schema).alias("data")) \
    .select("data.*")

# עיבוד הנתונים (פילטרים לדוגמה)
silver_stream_df = parsed_df.filter(col("value") > 100)

# כתיבה ל‑Silver
silver_stream_df.writeStream \
    .format("parquet") \
    .option("checkpointLocation", "/tmp/checkpoints/silver") \
    .option("path", "s3a://bucket-silver/silver_data.parquet") \
    .outputMode("append") \
    .start() \
    .awaitTermination()
