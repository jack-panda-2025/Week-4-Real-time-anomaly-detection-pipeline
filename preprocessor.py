class DataPreprocessor:

    def __init__(self):
        # Normal ranges for each sensor metric
        self.limits = {"temperature": (20, 90), "pressure": (1, 9), "vibration": (0, 4)}

    def validate(self, data):
        """Check if all required fields exist"""
        required = ["timestamp", "sensor_id", "temperature", "pressure", "vibration"]
        for field in required:
            if field not in data:
                return False, f"Missing field: {field}"
        return True, "OK"

    def clean(self, data):
        """Round values and flag anomalies"""
        cleaned = {
            "timestamp": data["timestamp"],
            "sensor_id": data["sensor_id"],
            "temperature": round(data["temperature"], 2),
            "pressure": round(data["pressure"], 2),
            "vibration": round(data["vibration"], 2),
            "is_anomaly": False,
        }

        # Flag anomaly if any value is out of range
        for metric, (low, high) in self.limits.items():
            if not (low <= cleaned[metric] <= high):
                cleaned["is_anomaly"] = True
                cleaned["anomaly_reason"] = f"{metric} out of range: {cleaned[metric]}"
                break

        return cleaned

    def process(self, data):
        valid, msg = self.validate(data)
        if not valid:
            return None, msg
        return self.clean(data), "OK"
