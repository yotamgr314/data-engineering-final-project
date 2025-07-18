from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# הגדרת SparkSession
spark = SparkSession.builder \
    .appName("bronze_to_silver_batch") \
    .getOrCreate()

# קריאה מקובץ פרקט
bronze_df = spark.read.parquet("s3a://bucket-bronze/bronze_data.parquet")

# עיבוד נתונים (לדוגמה: פילטרים, המרת תאריכים)
silver_df = bronze_df.filter(col("value") > 100)

# כתיבה ל‑Silver
silver_df.write.parquet("s3a://bucket-silver/silver_data.parquet", mode="overwrite")
