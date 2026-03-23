import pickle
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Generate training data (normal sensor readings)
np.random.seed(42)
n_samples = 1000

training_data = np.column_stack(
    [
        np.random.uniform(20, 90, n_samples),  # temperature (normal range)
        np.random.uniform(1, 9, n_samples),  # pressure (normal range)
        np.random.uniform(0, 4, n_samples),  # vibration (normal range)
    ]
)

# Train scaler
scaler = StandardScaler()
training_scaled = scaler.fit_transform(training_data)

# Train Isolation Forest
model = IsolationForest(contamination=0.1, random_state=42)  # expect 10% anomalies
model.fit(training_scaled)

# Save model and scaler
with open("anomaly_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

print("Model trained and saved!")
print(f"Training samples: {n_samples}")
