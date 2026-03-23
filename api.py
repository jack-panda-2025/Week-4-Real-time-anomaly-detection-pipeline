from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from database import Database

app = FastAPI()
db = Database()


@app.get("/anomalies")
def get_anomalies():
    rows = db.get_recent_anomalies(limit=20)
    return [
        {
            "timestamp": str(row[0]),
            "sensor_id": row[1],
            "temperature": row[2],
            "pressure": row[3],
            "vibration": row[4],
            "anomaly_score": row[5],
        }
        for row in rows
    ]


@app.get("/stats")
def get_stats():
    cursor = db.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sensor_readings")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM sensor_readings WHERE is_anomaly = TRUE")
    anomalies = cursor.fetchone()[0]
    cursor.close()
    return {
        "total_readings": total,
        "total_anomalies": anomalies,
        "anomaly_rate": round(anomalies / total * 100, 2) if total > 0 else 0,
    }


@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>AI Anomaly Dashboard</title>
        <style>
            body { font-family: Arial; background: #1a1a2e; color: white; padding: 20px; }
            h1 { color: #e94560; }
            .stats { display: flex; gap: 20px; margin-bottom: 30px; }
            .stat-card { background: #16213e; padding: 20px; border-radius: 10px; flex: 1; text-align: center; }
            .stat-card h2 { color: #e94560; font-size: 2em; margin: 0; }
            table { width: 100%; border-collapse: collapse; background: #16213e; border-radius: 10px; }
            th { background: #e94560; padding: 10px; }
            td { padding: 10px; border-bottom: 1px solid #333; text-align: center; }
            tr:hover { background: #0f3460; }
        </style>
    </head>
    <body>
        <h1>🚨 AI Anomaly Detection Dashboard</h1>
        <div class="stats" id="stats"></div>
        <h2>Recent Anomalies</h2>
        <table>
            <thead>
                <tr>
                    <th>Timestamp</th>
                    <th>Sensor ID</th>
                    <th>Temperature</th>
                    <th>Pressure</th>
                    <th>Vibration</th>
                    <th>Anomaly Score</th>
                </tr>
            </thead>
            <tbody id="anomalies"></tbody>
        </table>
        <script>
            async function loadStats() {
                const res = await fetch('/stats');
                const data = await res.json();
                document.getElementById('stats').innerHTML = `
                    <div class="stat-card"><h2>${data.total_readings}</h2><p>Total Readings</p></div>
                    <div class="stat-card"><h2>${data.total_anomalies}</h2><p>Anomalies Detected</p></div>
                    <div class="stat-card"><h2>${data.anomaly_rate}%</h2><p>Anomaly Rate</p></div>
                `;
            }

            async function loadAnomalies() {
                const res = await fetch('/anomalies');
                const data = await res.json();
                document.getElementById('anomalies').innerHTML = data.map(row => `
                    <tr>
                        <td>${row.timestamp}</td>
                        <td>${row.sensor_id}</td>
                        <td>${row.temperature}</td>
                        <td>${row.pressure}</td>
                        <td>${row.vibration}</td>
                        <td>${row.anomaly_score}</td>
                    </tr>
                `).join('');
            }

            loadStats();
            loadAnomalies();
            setInterval(() => { loadStats(); loadAnomalies(); }, 5000);
        </script>
    </body>
    </html>
    """
