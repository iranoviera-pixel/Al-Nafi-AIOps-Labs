import psutil
import pandas as pd
from sklearn.ensemble import IsolationForest

def collect_metrics():
    metrics = {
        'cpu_percent': psutil.cpu_percent(),
        'memory_percent': psutil.virtual_memory().percent,
        'disk_usage': psutil.disk_usage('/').percent
    }
    return metrics

# Collect initial metrics
data = []
for _ in range(100):  # Collect 100 samples
    data.append(collect_metrics())
  
# Convert to DataFrame
df = pd.DataFrame(data)
print(df.describe())

# Train anomaly detection model
model = IsolationForest(contamination=0.1)
model.fit(df)

# Predict anomalies
df['anomaly'] = model.predict(df)
print(df[df['anomaly'] == -1])  # Show anomalies



