Lab 56: AI-Enhanced Linux Service Configuration and Automation

Objectives

By the end of this lab, you will be able to:

Identify and evaluate open-source AI tools for Linux system automation.
Develop a Python script leveraging machine learning to predict and configure system services.
Automate Linux service configuration using AI-driven approaches.
Understand the practical applications of AI in system administration.
Prerequisites

Basic knowledge of Linux command line
Python 3.x installed
pip package manager
A Linux system (Ubuntu/Debian recommended)
Basic understanding of machine learning concepts
Setup Requirements

Update your system:

sudo apt update && sudo apt upgrade -y
Install required packages:

sudo apt install python3-pip python3-venv -y
Create and activate a Python virtual environment:

python3 -m venv ai_automation
source ai_automation/bin/activate
Task 1: Research AI Tools for System Configuration Automation

Subtask 1.1: Identify Open-Source AI Tools

Research and list open-source AI tools suitable for system automation:

Ansible (with AI plugins)
TensorFlow Decision Forests
Scikit-learn for predictive modeling
PyTorch for custom models
Subtask 1.2: Evaluate Tools

Compare tools based on:

Ease of integration with Linux
Community support
Documentation quality
Expected Outcome: A shortlist of 2-3 tools with justification for selection.

Task 2: Develop a Machine Learning-Based Configuration Script

Subtask 2.1: Collect Historical Data

Create a sample dataset (service_usage.csv) with past service usage:

timestamp,cpu_usage,memory_usage,service_active
2023-01-01 08:00,45,70,1
2023-01-01 09:00,60,80,1
2023-01-01 10:00,30,50,0
Subtask 2.2: Train a Predictive Model

Install required libraries:

pip install pandas scikit-learn
Python script (train_model.py):

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

# Load data
data = pd.read_csv('service_usage.csv')
X = data[['cpu_usage', 'memory_usage']]
y = data['service_active']

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'service_predictor.joblib')
print("Model trained and saved!")
Expected Outcome: A trained model file (service_predictor.joblib).

Task 3: Automate Service Configuration

Subtask 3.1: Create Configuration Script

Python script (auto_configure.py):

import joblib
import psutil
import subprocess

# Load model
model = joblib.load('service_predictor.joblib')

# Get current metrics
cpu = psutil.cpu_percent()
mem = psutil.virtual_memory().percent

# Predict
prediction = model.predict([[cpu, mem]])

# Configure service
service = "apache2"  # Example service
if prediction[0] == 1:
    subprocess.run(["sudo", "systemctl", "start", service])
else:
    subprocess.run(["sudo", "systemctl", "stop", service])
Subtask 3.2: Schedule Automation

Add to crontab to run every hour:

(crontab -l 2>/dev/null; echo "0 * * * * /path/to/auto_configure.py") | crontab -
Expected Outcome: The script automatically starts/stops services based on system load.

Troubleshooting Tips

Permission Issues: Ensure the script has executable permissions (chmod +x auto_configure.py).
Model Errors: Verify the input data format matches training data.
Service Not Found: Check if the service name is correct in your system.
Conclusion

In this lab, you:

Researched AI tools for Linux automation.
Created a machine learning model to predict service needs.
Implemented an automated configuration system.
Key Takeaways:

AI can significantly enhance system administration tasks.
Open-source tools make AI accessible for automation.
Predictive models can optimize resource usage in real-time.
Next Steps:

Expand the model with more metrics (disk I/O, network usage).
Implement logging for the automation process.
Explore integration with configuration management tools like Ansible.

