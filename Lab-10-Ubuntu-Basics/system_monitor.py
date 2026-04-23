import psutil
import pandas as pd
from sklearn.ensemble import IsolationForest

# Collect system metrics
def collect_metrics():
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory().percent
    return {'cpu': cpu, 'ram': ram}

# Anomaly detection
def detect_anomaly(metrics_history):
    model = IsolationForest(contamination=0.1)
    df = pd.DataFrame(metrics_history)
    model.fit(df)
    return model.predict(df)

if __name__ == "__main__":
    metrics_history = []
    for _ in range(10):  # Simulate 10 iterations
        metrics = collect_metrics()
        metrics_history.append(metrics)
        print(f"CPU: {metrics['cpu']}%, RAM: {metrics['ram']}%")
    
    anomalies = detect_anomaly(metrics_history)
    print("Anomalies detected:", anomalies)


