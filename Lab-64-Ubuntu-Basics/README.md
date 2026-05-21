Lab 64: AI-Driven Threat Detection and Security Automation

Objectives

By the end of this lab, you will be able to:

Identify open-source AI-driven security tools for Linux.
Implement a Python script to detect anomalies in system logs using machine learning.
Automate security patch management based on AI recommendations.
Prerequisites

A Linux system (Ubuntu 22.04 recommended)
Python 3.8 or later
Basic knowledge of Linux commands and Python programming
pip installed for Python package management
Task 1: Research AI-Driven Security Tools for Linux

Subtask 1.1: Explore Open-Source AI Security Solutions

Open a terminal and research the following tools:

Wazuh: An open-source SIEM with ML capabilities.
OSSEC: Host-based intrusion detection system (HIDS).
Suricata: Network threat detection with ML support.
Install Wazuh for demonstration:

curl -sO https://packages.wazuh.com/4.7/wazuh-install.sh && sudo bash ./wazuh-install.sh --all-in-one
Expected Outcome:
Wazuh dashboard accessible at http://<your-server-IP>:5601.

Troubleshooting:

Ensure ports 5601 (Kibana) and 1515 (Wazuh) are open in your firewall.
Task 2: Implement a Python Script for Anomaly Detection in System Logs

Subtask 2.1: Set Up Python Environment

Install required libraries:
pip install pandas scikit-learn numpy
Subtask 2.2: Create a Log Anomaly Detector

Save the following script as log_analyzer.py:
import pandas as pd
from sklearn.ensemble import IsolationForest

# Sample log data (replace with real log paths)
logs = [
    {"timestamp": "2023-10-01 12:00", "event": "login", "user": "admin", "ip": "192.168.1.1"},
    {"timestamp": "2023-10-01 12:05", "event": "failed_login", "user": "root", "ip": "10.0.0.1"}
]
df = pd.DataFrame(logs)

# Feature engineering
df['is_failed'] = df['event'].apply(lambda x: 1 if 'failed' in x else 0)

# Train Isolation Forest model
model = IsolationForest(contamination=0.1)
model.fit(df[['is_failed']])

# Predict anomalies
df['anomaly'] = model.predict(df[['is_failed']])
print(df[df['anomaly'] == -1])  # -1 indicates anomaly
Expected Outcome:
The script outputs log entries flagged as anomalous (e.g., repeated failed logins).

Key Concept:
Isolation Forest is an unsupervised ML algorithm for anomaly detection.

Task 3: Automate Security Patching Based on AI Recommendations

Subtask 3.1: Integrate with Package Management

Create a script auto_patch.py:
import subprocess
import requests

# Mock AI API (replace with actual AI service)
def check_vulnerabilities():
    return ["CVE-2023-1234"]  # Example CVE

vulnerabilities = check_vulnerabilities()
if vulnerabilities:
    subprocess.run(["sudo", "apt-get", "update"])
    subprocess.run(["sudo", "apt-get", "upgrade", "-y"])
    print(f"Patched {len(vulnerabilities)} vulnerabilities.")
Subtask 3.2: Schedule with Cron

Add to crontab (crontab -e):
0 3 * * * /usr/bin/python3 /path/to/auto_patch.py >> /var/log/patch.log
Expected Outcome:
Automatic patching at 3 AM daily, logged in /var/log/patch.log.
