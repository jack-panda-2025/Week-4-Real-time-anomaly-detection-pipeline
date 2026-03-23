import pickle
import numpy as np


class AnomalyDetector:

    def __init__(self):
        with open("anomaly_model.pkl", "rb") as f:
            self.model = pickle.load(f)
        with open("scaler.pkl", "rb") as f:
            self.scaler = pickle.load(f)
        print("Model loaded!")

    def predict(self, data):
        features = np.array(
            [[data["temperature"], data["pressure"], data["vibration"]]]
        )

        scaled = self.scaler.transform(features)
        prediction = self.model.predict(scaled)
        score = self.model.score_samples(scaled)[0]

        return {
            "is_anomaly": bool(prediction[0] == -1),  # -1 = anomaly, 1 = normal
            "anomaly_score": round(score, 4),
        }
