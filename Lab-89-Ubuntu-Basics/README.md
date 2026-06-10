Lab 89: AI-Powered Predictive Monitoring and Anomaly Detection

Objectives

By the end of this lab, you will be able to:

Understand AI-based monitoring tools and their applications
Implement a Python script for anomaly detection using machine learning
Integrate AI-driven anomaly detection with Nagios for real-time monitoring
Analyze system metrics and predict anomalies using historical data
Prerequisites

Basic knowledge of Python programming
Familiarity with Linux command line
Python 3.6+ installed
Nagios Core installed (optional for Task 3))
Access to a Linux system (Ubuntu/Debian recommended)
Task 1: Research AI-Based Monitoring Tools

Subtask 1.1: Explore Open-Source AI Monitoring Tools

Research the following open-source tools:

Prometheus + Grafana: For metrics collection and visualization
Elastic Stack (ELK): For log analysis and anomaly detection
Apache Spot: For network anomaly detection
PyOD: Python library for outlier detection
Compare their features:

Real-time monitoring capabilities
Machine learning integration
Ease of deployment
Expected Outcome:
A list of 2-3 tools that support AI-driven anomaly detection.

Task 2: Implement a Python Script for Anomaly Detection

Subtask 2.1: Install Required Python Libraries

Run the following commands to install necessary packages:

pip install pandas numpy scikit-learn pyod matplotlib
Subtask 2.2: Generate/Collect Sample System Data

Use the following Python script to generate synthetic system metrics (CPU usage):

import pandas as pd
import numpy as np

# Generate synthetic CPU usage (normal behavior with some outliers)
np.random.seed(42)
normal_data = np.random.normal(loc=50, scale=10, size=200)  # Normal CPU usage (50% ± 10%)
outliers = np.random.uniform(low=90, high=100, size=10)     # Anomalous CPU spikes
cpu_data = np.concatenate([normal_data, outliers])
np.random.shuffle(cpu_data)

# Save to CSV
df = pd.DataFrame(cpu_data, columns=['CPU_Usage'])
df.to_csv('system_metrics.csv', index=False)
print("Sample data saved to 'system_metrics.csv'")
Expected Outcome:
A CSV file (system_metrics.csv) containing CPU usage data with anomalies.

Subtask 2.3: Train an Anomaly Detection Model

Use the Isolation Forest algorithm from sklearn:

from sklearn.ensemble import IsolationForest
import pandas as pd

# Load data
data = pd.read_csv('system_metrics.csv')
X = data[['CPU_Usage']].values

# Train model
model = IsolationForest(contamination=0.05, random_state=42)  # 5% outliers expected
model.fit(X)

# Predict anomalies
data['Anomaly'] = model.predict(X)
data['Anomaly'] = data['Anomaly'].apply(lambda x: 1 if x == -1 else 0)  # Convert to binary

# Save results
data.to_csv('anomaly_results.csv', index=False)
print("Anomaly detection results saved to 'anomaly_results.csv'")
Expected Outcome:
A CSV file (anomaly_results.csv) with a binary column indicating anomalies (1 = anomaly, 0 = normal).

Subtask 2.4: Visualize Anomalies

Plot anomalies using matplotlib:

import matplotlib.pyplot as plt

# Load results
results = pd.read_csv('anomaly_results.csv')

# Plot
plt.figure(figsize=(10, 6))
normal = results[results['Anomaly'] == 0]
anomalies = results[results['Anomaly'] == 1]

plt.scatter(normal.index, normal['CPU_Usage'], color='blue', label='Normal')
plt.scatter(anomalies.index, anomalies['CPU_Usage'], color='red', label='Anomaly')
plt.xlabel('Time')
plt.ylabel('CPU Usage (%)')
plt.title('Anomaly Detection Results')
plt.legend()
plt.savefig('anomaly_plot.png')
plt.show()
Expected Outcome:
A plot (anomaly_plot.png) showing CPU usage with anomalies highlighted in red.

Task 3: Integrate with Nagios Monitoring

Subtask 3.1: Set Up Nagios Plugin Directory

Navigate to Nagios plugins directory:

cd /usr/local/nagios/libexec
Create a Python script check_anomaly.py:

#!/usr/bin/env python3
import pandas as pd
from sklearn.ensemble import IsolationForest
import sys

# Load latest data (replace with actual data source)
data = pd.read_csv('/path/to/system_metrics.csv')
X = data[['CPU_Usage']].values[-50:]  # Last 50 samples

# Load pre-trained model
model = IsolationForest(contamination=0.05, random_state=42)
model.fit(X)

# Predict
pred = model.predict(X[-1].reshape(1, -1))  # Check latest sample

if pred == -1:
    print("CRITICAL: Anomaly detected in CPU usage!")
    sys.exit(2)
else:
    print("OK: No anomalies detected")
    sys.exit(0)
Make the script executable:

chmod +x check_anomaly.py
Subtask 3.2: Add Custom Check to Nagios

Edit Nagios commands configuration:

sudo nano /usr/local/nagios/etc/objects/commands.cfg
Add the following:

define command {
    command_name    check_anomaly
    command_line    /usr/local/nagios/libexec/check_anomaly.py
}
Define a service in localhost.cfg:

define service {
    use                 generic-service
    host_name           localhost
    service_description CPU_Anomaly_Detection
    check_command       check_anomaly
    check_interval     5  # Check every 5 minutes
}
Restart Nagios:

sudo systemctl restart nagios
Expected Outcome:
Nagios will now alert when the AI model detects CPU anomalies.
