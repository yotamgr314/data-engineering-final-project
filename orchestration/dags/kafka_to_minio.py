from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from kafka import KafkaConsumer
import json
import pandas as pd
import boto3
from io import StringIO
import os

DEFAULT_ARGS = {
    'owner': 'airflow',
}

BROKER = os.environ.get('KAFKA_BROKER', 'kafka:9092')
TOPIC = os.environ.get('TOPIC', 'bronze-topic')
S3_ENDPOINT = os.environ.get('S3_ENDPOINT', 'http://minio:9000')
S3_BUCKET = os.environ.get('BRONZE_BUCKET', 'bronze')
ACCESS_KEY = os.environ.get('MINIO_ACCESS_KEY', 'minioadmin')
SECRET_KEY = os.environ.get('MINIO_SECRET_KEY', 'minioadmin')


def consume_and_store():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BROKER,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=1000,
    )

    records = [msg.value for msg in consumer]
    if not records:
        print('No messages consumed')
        return

    df = pd.DataFrame(records)
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, index=False)

    s3 = boto3.client(
        's3',
        endpoint_url=S3_ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    if S3_BUCKET not in [b['Name'] for b in s3.list_buckets().get('Buckets', [])]:
        s3.create_bucket(Bucket=S3_BUCKET)

    s3.put_object(Bucket=S3_BUCKET, Key='bronze_data.csv', Body=csv_buffer.getvalue())
    print('Wrote data to MinIO bucket', S3_BUCKET)


with DAG(
    dag_id='kafka_to_minio',
    default_args=DEFAULT_ARGS,
    start_date=datetime(2023, 1, 1),
    schedule_interval='@hourly',
    catchup=False,
) as dag:
    consume_task = PythonOperator(
        task_id='consume_and_store',
        python_callable=consume_and_store,
    )
