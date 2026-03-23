import json
import random
import time
from datetime import datetime
from kafka import KafkaProducer

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)


def generate_sensor_data():
    return {
        "timestamp": datetime.now().isoformat(),
        "sensor_id": random.randint(1, 10),
        "temperature": random.uniform(20, 100),
        "pressure": random.uniform(1, 10),
        "vibration": random.uniform(0, 5),
    }


print("Starting producer...")
while True:
    data = generate_sensor_data()
    producer.send("sensor-data", data)
    print(f"Sent: {data}")
    time.sleep(1)
