FROM python:3.10-slim
WORKDIR /app
COPY producer.py /app/
COPY requirements.txt /app/
COPY data /app/data
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "producer.py"]
