import json
from kafka import KafkaConsumer
from preprocessor import DataPreprocessor
from anomaly_detector import AnomalyDetector
from database import Database

consumer = KafkaConsumer(
    "sensor-data",
    bootstrap_servers=["localhost:9092"],
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset="latest",
)

preprocessor = DataPreprocessor()
detector = AnomalyDetector()
db = Database()

print("Starting consumer with DB storage...")
for message in consumer:
    raw = message.value
    cleaned, msg = preprocessor.process(raw)

    if cleaned is None:
        print(f"Invalid data: {msg}")
        continue

    result = detector.predict(cleaned)
    db.insert(cleaned, result)

    if result["is_anomaly"]:
        print(
            f"🚨 ANOMALY saved! sensor={cleaned['sensor_id']} score={result['anomaly_score']}"
        )
    else:
        print(f"✅ Normal saved: sensor={cleaned['sensor_id']}")
