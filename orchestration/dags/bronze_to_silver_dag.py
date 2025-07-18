from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import os

# פונקציות לעיבוד
def run_batch_processing():
    # הפעלת עיבוד Batch
    os.system("spark-submit --master spark://spark-master:7077 --packages org.apache.hadoop:hadoop-aws:3.3.4 bronze_to_silver_batch.py")

def run_stream_processing():
    # הפעלת עיבוד Stream
    os.system("spark-submit --master spark://spark-master:7077 --packages org.apache.hadoop:hadoop-aws:3.3.4 bronze_to_silver_stream.py")

# הגדרת DAG
dag = DAG(
    'bronze_to_silver_dag',
    description='DAG to process bronze to silver data',
    schedule_interval='@daily',
    start_date=datetime(2025, 7, 18),
    catchup=False,
)

# הגדרת משימות
batch_task = PythonOperator(
    task_id='run_batch_processing',
    python_callable=run_batch_processing,
    dag=dag,
)

stream_task = PythonOperator(
    task_id='run_stream_processing',
    python_callable=run_stream_processing,
    dag=dag,
)

batch_task >> stream_task  # הגדרת סדר ביצוע
