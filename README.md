# Data Engineering Final Project

This repository contains a minimal streaming setup with Kafka and a basic orchestration layer using Apache Airflow. A small Kafka producer reads CSV files and publishes them to Kafka. An Airflow DAG consumes those records and writes them to a MinIO bucket to represent the bronze Iceberg layer.

## Prerequisites
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

## Start the Services
Each component has its own compose file.

### Streaming (Kafka + Producer)
```
cd streaming
docker compose up --build
```
This starts ZooKeeper, Kafka and the sample producer which publishes records from `data/bronze_data.csv` to the `bronze-topic` topic.

### Orchestration (Airflow)
```
cd orchestration
docker compose up
```
Access the Airflow UI at [http://localhost:8080](http://localhost:8080). Enable the `kafka_to_minio` DAG to start consuming records from Kafka and writing them to the `bronze` bucket on the MinIO service (make sure a MinIO instance is available on `http://minio:9000`).

### Spark (optional)
A minimal Spark compose file is provided in `processing/docker-compose.yml`.
```
cd processing
docker compose up
```

## Sample Data
The sample CSV used by the producer is located in `streaming/data/bronze_data.csv`. Feel free to modify or replace it with your own data.

## Running the Pipeline
1. Start the streaming services to begin sending messages.
2. Start Airflow and enable the DAG.
3. Messages will be consumed and stored in the MinIO `bronze` bucket as `bronze_data.csv`.

