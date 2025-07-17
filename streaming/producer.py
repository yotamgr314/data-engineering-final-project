import csv, json, os, time
from kafka import KafkaProducer

BROKER     = os.environ.get('KAFKA_BROKER', 'kafka:9092')
TOPIC      = os.environ.get('TOPIC', 'bronze-topic')
CSV_PATH   = os.environ.get('CSV_PATH', 'data/bronze_data.csv')

producer = KafkaProducer(
    bootstrap_servers=BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def main():
    with open(CSV_PATH, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            producer.send(TOPIC, row)
            producer.flush()
            print(f"Sent to {TOPIC}: {row}")
            time.sleep(1)

if __name__ == "__main__":
    main()
