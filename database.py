import psycopg2
from datetime import datetime


class Database:

    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="sensordb",
            user="admin",
            password="admin123",
        )
        self.create_table()
        print("Database connected!")

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMP,
                sensor_id INTEGER,
                temperature FLOAT,
                pressure FLOAT,
                vibration FLOAT,
                is_anomaly BOOLEAN,
                anomaly_score FLOAT,
                created_at TIMESTAMP DEFAULT NOW()
            )
        """
        )
        self.conn.commit()
        cursor.close()

    def insert(self, data, result):
        cursor = self.conn.cursor()
        cursor.execute(
            """
    INSERT INTO sensor_readings 
    (timestamp, sensor_id, temperature, pressure, vibration, is_anomaly, anomaly_score)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
""",
            (
                data["timestamp"],
                data["sensor_id"],
                data["temperature"],
                data["pressure"],
                data["vibration"],
                bool(result["is_anomaly"]),  # ← must be bool
                float(result["anomaly_score"]),  # ← must be float
            ),
        )
        self.conn.commit()
        cursor.close()

    def get_recent_anomalies(self, limit=10):
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT timestamp, sensor_id, temperature, pressure, vibration, anomaly_score
            FROM sensor_readings
            WHERE is_anomaly = TRUE
            ORDER BY created_at DESC
            LIMIT %s
        """,
            (limit,),
        )
        rows = cursor.fetchall()
        cursor.close()
        return rows
