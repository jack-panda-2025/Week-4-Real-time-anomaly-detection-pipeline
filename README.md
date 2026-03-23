# Real-time Anomaly Detection Pipeline

A full-stack streaming pipeline for real-time sensor anomaly detection, built with Kafka, Scikit-learn, PostgreSQL, and FastAPI.

## Architecture

```
Producer → Kafka → Consumer → Preprocessor → ML Model → PostgreSQL → FastAPI → Dashboard
```

| Component | File | Role |
|-----------|------|------|
| Producer | `producer.py` | Simulates sensor readings, publishes to Kafka |
| Consumer | `consumer.py` | Orchestrates the end-to-end pipeline |
| Preprocessor | `preprocessor.py` | Validates and cleans incoming data |
| Anomaly Detector | `anomaly_detector.py` | Isolation Forest ML model inference |
| Database | `database.py` | PostgreSQL read/write layer |
| API + Dashboard | `api.py` | FastAPI server with live web dashboard |
| Model Training | `train_model.py` | Offline training script for the ML model |

## Tech Stack

- **Streaming**: Apache Kafka (via Docker)
- **ML**: Scikit-learn — Isolation Forest + StandardScaler
- **Storage**: PostgreSQL 15
- **API**: FastAPI + Uvicorn
- **Containerization**: Docker Compose
- **Language**: Python 3.12

## Quick Start

### 1. Start infrastructure

```bash
docker compose up -d
```

This starts Kafka (port 9092) and PostgreSQL (port 5432).

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Train the model

```bash
python train_model.py
```

Outputs `anomaly_model.pkl` and `scaler.pkl`.

### 4. Start the pipeline (3 terminals)

```bash
# Terminal 1 — consumer (processes Kafka messages)
python consumer.py

# Terminal 2 — producer (generates sensor data)
python producer.py

# Terminal 3 — API server
uvicorn api:app --reload --port 8000
```

### 5. Open the dashboard

Visit [http://localhost:8000](http://localhost:8000) — auto-refreshes every 5 seconds.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Live monitoring dashboard (HTML) |
| GET | `/anomalies` | Last 20 detected anomalies (JSON) |
| GET | `/stats` | Total readings, anomaly count, anomaly rate (JSON) |

## How It Works

### Data Generation
`producer.py` publishes simulated sensor readings to the `sensor-data` Kafka topic once per second:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "sensor_id": 3,
  "temperature": 75.42,
  "pressure": 6.18,
  "vibration": 2.93
}
```

### Two-Stage Anomaly Detection
The consumer runs each message through two detection layers:

1. **Rule-based (Preprocessor)**: Flags readings outside defined normal ranges
   - Temperature: 20–90 °C
   - Pressure: 1–9 units
   - Vibration: 0–4 units

2. **ML-based (Isolation Forest)**: Detects statistical anomalies in the feature space using a model trained on normal operating data

Both results are stored in PostgreSQL along with the anomaly confidence score.

### ML Model
- Algorithm: **Isolation Forest** (unsupervised)
- Features: `temperature`, `pressure`, `vibration`
- Training data: 1,000 synthetic normal readings
- Contamination rate: 10%
- Preprocessing: `StandardScaler` normalization

## Database Schema

```sql
CREATE TABLE sensor_readings (
    id           SERIAL PRIMARY KEY,
    timestamp    TIMESTAMP,
    sensor_id    INTEGER,
    temperature  FLOAT,
    pressure     FLOAT,
    vibration    FLOAT,
    is_anomaly   BOOLEAN,
    anomaly_score FLOAT,
    created_at   TIMESTAMP DEFAULT NOW()
);
```

Database: `sensordb` | User: `admin` | Port: `5432`

## Project Structure

```
week4-realtime-ai/
├── producer.py           # Kafka data producer
├── consumer.py           # Pipeline orchestrator
├── preprocessor.py       # Data validation & cleaning
├── anomaly_detector.py   # ML inference (Isolation Forest)
├── database.py           # PostgreSQL data layer
├── api.py                # FastAPI server + dashboard
├── train_model.py        # Offline model training
├── anomaly_model.pkl     # Trained Isolation Forest model
├── scaler.pkl            # Fitted StandardScaler
└── docker-compose.yml    # Kafka + PostgreSQL services
```
