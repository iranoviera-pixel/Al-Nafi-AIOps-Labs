Lab 70: AI-Driven Automation and Optimization with Ansible

Lab Objectives

By the end of this lab, students will be able to:

Understand the fundamentals of AI-driven automation in infrastructure management
Research and identify AI tools that integrate with Ansible for predictive automation
Implement a Python-based machine learning script to predict system requirements
Create dynamic Ansible playbooks that adapt based on AI-driven insights
Optimize automation tasks using machine learning predictions
Apply AI-enhanced automation to real-world infrastructure scenarios
Prerequisites

Before starting this lab, students should have:

Basic understanding of Linux command line operations
Fundamental knowledge of Ansible playbooks and YAML syntax
Basic Python programming skills
Understanding of system monitoring concepts (CPU, memory, disk usage)
Familiarity with package management in Linux
Lab Environment Setup

Ready-to-Use Cloud Machines: Al Nafi provides pre-configured Linux-based cloud machines for this lab. Simply click Start Lab to access your environment. No need to build your own virtual machine or install additional software - everything is ready to use.

Your lab environment includes:

Ubuntu 20.04 LTS with Python 3.8+
Ansible 4.0+ pre-installed
Required Python libraries for machine learning
Sample system monitoring data
Text editors (nano, vim)
Task 1: Research AI Tools for Ansible Integration

Subtask 1.1: Understanding AI-Driven Automation Concepts

First, let's explore what AI-driven automation means in the context of infrastructure management.

Connect to your lab environment and open a terminal

Create a project directory for our lab work:

mkdir ~/ai-ansible-lab
cd ~/ai-ansible-lab
Create a research document to track our findings:
nano ai-tools-research.md
Add the following content to understand key concepts:
# AI-Driven Automation Research

## Key Concepts:
- Predictive Scaling: Using historical data to predict resource needs
- Anomaly Detection: Identifying unusual system behavior patterns
- Intelligent Configuration: Automatically adjusting configurations based on workload patterns
- Proactive Maintenance: Predicting and preventing system failures

## Open Source AI Tools for Ansible:
1. Scikit-learn: Machine learning library for Python
2. Pandas: Data manipulation and analysis
3. NumPy: Numerical computing
4. Matplotlib: Data visualization
5. Ansible Runner: Programmatic interface for Ansible
Save and exit the file (Ctrl+X, then Y, then Enter)
Subtask 1.2: Setting Up the Python Environment

Verify Python installation:
python3 --version
pip3 --version
Install required Python packages:
pip3 install scikit-learn pandas numpy matplotlib ansible-runner
Verify installations:
python3 -c "import sklearn, pandas, numpy, matplotlib; print('All packages installed successfully')"
Task 2: Implement Machine Learning for System Prediction

Subtask 2.1: Create Sample System Monitoring Data

Create a data generation script:
nano generate_system_data.py
Add the following Python script:
#!/usr/bin/env python3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

def generate_system_data():
    """Generate sample system monitoring data for the past 30 days"""
    
    # Set random seed for reproducible results
    np.random.seed(42)
    
    # Generate timestamps for the past 30 days (hourly data)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    timestamps = pd.date_range(start=start_date, end=end_date, freq='H')
    
    data = []
    
    for i, timestamp in enumerate(timestamps):
        # Simulate daily patterns (higher usage during business hours)
        hour = timestamp.hour
        day_of_week = timestamp.weekday()
        
        # Base load with daily and weekly patterns
        base_cpu = 20 + 30 * np.sin(2 * np.pi * hour / 24) + 10 * (day_of_week < 5)
        base_memory = 40 + 20 * np.sin(2 * np.pi * hour / 24) + 15 * (day_of_week < 5)
        base_disk = 60 + 10 * np.sin(2 * np.pi * hour / 24)
        
        # Add random noise
        cpu_usage = max(0, min(100, base_cpu + np.random.normal(0, 10)))
        memory_usage = max(0, min(100, base_memory + np.random.normal(0, 8)))
        disk_usage = max(0, min(100, base_disk + np.random.normal(0, 5)))
        
        # Simulate network traffic
        network_in = max(0, 100 + 200 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 50))
        network_out = max(0, 80 + 150 * np.sin(2 * np.pi * hour / 24) + np.random.normal(0, 40))
        
        data.append({
            'timestamp': timestamp.isoformat(),
            'cpu_usage': round(cpu_usage, 2),
            'memory_usage': round(memory_usage, 2),
            'disk_usage': round(disk_usage, 2),
            'network_in_mbps': round(network_in, 2),
            'network_out_mbps': round(network_out, 2),
            'hour': hour,
            'day_of_week': day_of_week,
            'is_weekend': day_of_week >= 5
        })
    
    return pd.DataFrame(data)

if __name__ == "__main__":
    # Generate the data
    df = generate_system_data()
    
    # Save to CSV
    df.to_csv('system_monitoring_data.csv', index=False)
    print(f"Generated {len(df)} data points and saved to system_monitoring_data.csv")
    
    # Display basic statistics
    print("\nData Summary:")
    print(df[['cpu_usage', 'memory_usage', 'disk_usage']].describe())
Run the data generation script:
python3 generate_system_data.py
Verify the generated data:
head -10 system_monitoring_data.csv
wc -l system_monitoring_data.csv
Subtask 2.2: Create the Machine Learning Prediction Script

Create the main ML prediction script:
nano ml_system_predictor.py
Add the comprehensive ML script:
#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
import json
import pickle
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class SystemResourcePredictor:
    def __init__(self):
        self.models = {}
        self.feature_columns = ['hour', 'day_of_week', 'is_weekend', 
                               'cpu_usage_lag1', 'memory_usage_lag1', 'disk_usage_lag1']
        self.target_columns = ['cpu_usage', 'memory_usage', 'disk_usage']
        
    def prepare_features(self, df):
        """Prepare features for machine learning"""
        df = df.copy()
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Create lag features (previous hour's values)
        for col in self.target_columns:
            df[f'{col}_lag1'] = df[col].shift(1)
        
        # Drop rows with NaN values (first row due to lag)
        df = df.dropna()
        
        return df
    
    def train_models(self, data_file='system_monitoring_data.csv'):
        """Train machine learning models for each resource type"""
        print("Loading and preparing data...")
        df = pd.read_csv(data_file)
        df = self.prepare_features(df)
        
        # Prepare features and targets
        X = df[self.feature_columns]
        
        print("Training models for each resource type...")
        for target in self.target_columns:
            print(f"  Training model for {target}...")
            
            y = df[target]
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, shuffle=False
            )
            
            # Train Random Forest model
            model = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                max_depth=10,
                min_samples_split=5
            )
            model.fit(X_train, y_train)
            
            # Evaluate model
            y_pred = model.predict(X_test)
            mae = mean_absolute_error(y_test, y_pred)
            rmse = np.sqrt(mean_squared_error(y_test, y_pred))
            
            print(f"    MAE: {mae:.2f}, RMSE: {rmse:.2f}")
            
            # Store model
            self.models[target] = model
        
        # Save models
        with open('trained_models.pkl', 'wb') as f:
            pickle.dump(self.models, f)
        
        print("Models trained and saved successfully!")
    
    def load_models(self):
        """Load pre-trained models"""
        try:
            with open('trained_models.pkl', 'rb') as f:
                self.models = pickle.load(f)
            print("Models loaded successfully!")
        except FileNotFoundError:
            print("No trained models found. Please train models first.")
            return False
        return True
    
    def predict_next_hour(self, current_metrics):
        """Predict resource usage for the next hour"""
        if not self.models:
            if not self.load_models():
                return None
        
        # Get current time features
        now = datetime.now()
        next_hour = now + timedelta(hours=1)
        
        # Prepare features
        features = np.array([[
            next_hour.hour,
            next_hour.weekday(),
            1 if next_hour.weekday() >= 5 else 0,
            current_metrics['cpu_usage'],
            current_metrics['memory_usage'],
            current_metrics['disk_usage']
        ]])
        
        # Make predictions
        predictions = {}
        for target in self.target_columns:
            pred = self.models[target].predict(features)[0]
            predictions[target] = max(0, min(100, pred))  # Clamp between 0-100
        
        return predictions
    
    def generate_ansible_config(self, predictions, thresholds=None):
        """Generate Ansible configuration based on predictions"""
        if thresholds is None:
            thresholds = {
                'cpu_usage': {'high': 80, 'medium': 60},
                'memory_usage': {'high': 85, 'medium': 70},
                'disk_usage': {'high': 90, 'medium': 80}
            }
        
        config = {
            'predicted_metrics': predictions,
            'recommendations': [],
            'ansible_vars': {}
        }
        
        # CPU recommendations
        if predictions['cpu_usage'] > thresholds['cpu_usage']['high']:
            config['recommendations'].append("High CPU usage predicted - consider scaling up")
            config['ansible_vars']['cpu_scaling_action'] = 'scale_up'
            config['ansible_vars']['target_cpu_instances'] = 2
        elif predictions['cpu_usage'] > thresholds['cpu_usage']['medium']:
            config['recommendations'].append("Medium CPU usage predicted - monitor closely")
            config['ansible_vars']['cpu_scaling_action'] = 'monitor'
            config['ansible_vars']['target_cpu_instances'] = 1
        else:
            config['ansible_vars']['cpu_scaling_action'] = 'maintain'
            config['ansible_vars']['target_cpu_instances'] = 1
        
        # Memory recommendations
        if predictions['memory_usage'] > thresholds['memory_usage']['high']:
            config['recommendations'].append("High memory usage predicted - increase memory allocation")
            config['ansible_vars']['memory_action'] = 'increase'
            config['ansible_vars']['target_memory_gb'] = 8
        elif predictions['memory_usage'] > thresholds['memory_usage']['medium']:
            config['recommendations'].append("Medium memory usage predicted - prepare for scaling")
            config['ansible_vars']['memory_action'] = 'prepare'
            config['ansible_vars']['target_memory_gb'] = 4
        else:
            config['ansible_vars']['memory_action'] = 'maintain'
            config['ansible_vars']['target_memory_gb'] = 2
        
        # Disk recommendations
        if predictions['disk_usage'] > thresholds['disk_usage']['high']:
            config['recommendations'].append("High disk usage predicted - cleanup or expand storage")
            config['ansible_vars']['disk_action'] = 'expand'
            config['ansible_vars']['cleanup_enabled'] = True
        elif predictions['disk_usage'] > thresholds['disk_usage']['medium']:
            config['recommendations'].append("Medium disk usage predicted - schedule cleanup")
            config['ansible_vars']['disk_action'] = 'cleanup'
            config['ansible_vars']['cleanup_enabled'] = True
        else:
            config['ansible_vars']['disk_action'] = 'maintain'
            config['ansible_vars']['cleanup_enabled'] = False
        
        return config

def main():
    predictor = SystemResourcePredictor()
    
    print("=== AI-Driven System Resource Predictor ===\n")
    
    # Train models
    print("1. Training machine learning models...")
    predictor.train_models()
    
    # Simulate current system metrics
    current_metrics = {
        'cpu_usage': 45.5,
        'memory_usage': 62.3,
        'disk_usage': 78.9
    }
    
    print(f"\n2. Current system metrics:")
    for metric, value in current_metrics.items():
        print(f"   {metric}: {value}%")
    
    # Make predictions
    print("\n3. Predicting next hour resource usage...")
    predictions = predictor.predict_next_hour(current_metrics)
    
    if predictions:
        print("   Predictions for next hour:")
        for metric, value in predictions.items():
            print(f"   {metric}: {value:.2f}%")
        
        # Generate Ansible configuration
        print("\n4. Generating AI-driven Ansible configuration...")
        config = predictor.generate_ansible_config(predictions)
        
        # Save configuration
        with open('ai_ansible_config.json', 'w') as f:
            json.dump(config, f, indent=2)
        
        print("   Recommendations:")
        for rec in config['recommendations']:
            print(f"   - {rec}")
        
        print(f"\n   Configuration saved to ai_ansible_config.json")
        print("   Ansible variables generated for dynamic playbook execution")
    
    print("\n=== Prediction Complete ===")

if __name__ == "__main__":
    main()
Run the ML prediction script:
python3 ml_system_predictor.py
Examine the generated configuration:
cat ai_ansible_config.json
Task 3: Optimize Automation Tasks with AI-Driven Insights

Subtask 3.1: Create Dynamic Ansible Playbooks

Create an AI-enhanced Ansible playbook:
nano ai-optimized-playbook.yml
Add the dynamic playbook content:
---
- name: AI-Driven Infrastructure Optimization
  hosts: localhost
  gather_facts: yes
  vars_files:
    - ai_vars.yml
  
  tasks:
    - name: Display AI predictions
      debug:
        msg: |
          AI Predictions Summary:
          - Predicted CPU Usage: {{ predicted_cpu_usage }}%
          - Predicted Memory Usage: {{ predicted_memory_usage }}%
          - Predicted Disk Usage: {{ predicted_disk_usage }}%
          - Recommended Action: {{ cpu_scaling_action }}

    - name: CPU Scaling Decision
      debug:
        msg: "CPU scaling action: {{ cpu_scaling_action }}"
      when: cpu_scaling_action is defined

    - name: Scale up CPU resources (simulated)
      debug:
        msg: "Scaling up to {{ target_cpu_instances }} CPU instances"
      when: cpu_scaling_action == "scale_up"

    - name: Memory Management
      debug:
        msg: "Memory action: {{ memory_action }}, Target: {{ target_memory_gb }}GB"
      when: memory_action is defined

    - name: Increase memory allocation (simulated)
      debug:
        msg: "Increasing memory allocation to {{ target_memory_gb }}GB"
      when: memory_action == "increase"

    - name: Disk Cleanup Task
      debug:
        msg: "Performing disk cleanup as recommended by AI"
      when: cleanup_enabled | default(false)

    - name: Simulate disk cleanup
      shell: |
        echo "Simulating disk cleanup..."
        echo "Cleaning temporary files..."
        echo "Cleaning log files older than 30 days..."
        echo "Disk cleanup completed"
      when: cleanup_enabled | default(false)
      register: cleanup_result

    - name: Display cleanup results
      debug:
        var: cleanup_result.stdout_lines
      when: cleanup_enabled | default(false)

    - name: Generate optimization report
      copy:
        content: |
          AI-Driven Optimization Report
          ============================
          Timestamp: {{ ansible_date_time.iso8601 }}
          
          Predictions:
          - CPU Usage: {{ predicted_cpu_usage }}%
          - Memory Usage: {{ predicted_memory_usage }}%
          - Disk Usage: {{ predicted_disk_usage }}%
          
          Actions Taken:
          - CPU Scaling: {{ cpu_scaling_action }}
          - Memory Action: {{ memory_action }}
          - Disk Cleanup: {{ cleanup_enabled | default(false) }}
          
          Recommendations Applied:
          {% for recommendation in ai_recommendations %}
          - {{ recommendation }}
          {% endfor %}
        dest: ./optimization_report_{{ ansible_date_time.epoch }}.txt
      delegate_to: localhost
Create a script to convert AI predictions to Ansible variables:
nano convert_ai_to_ansible.py
Add the conversion script:
#!/usr/bin/env python3
import json
import yaml

def convert_ai_config_to_ansible_vars():
    """Convert AI configuration to Ansible variables file"""
    
    # Load AI configuration
    try:
        with open('ai_ansible_config.json', 'r') as f:
            ai_config = json.load(f)
    except FileNotFoundError:
        print("AI configuration file not found. Please run the ML predictor first.")
        return False
    
    # Extract predictions and variables
    predictions = ai_config['predicted_metrics']
    ansible_vars = ai_config['ansible_vars']
    recommendations = ai_config['recommendations']
    
    # Create Ansible variables
    vars_dict = {
        # Predictions
        'predicted_cpu_usage': round(predictions['cpu_usage'], 2),
        'predicted_memory_usage': round(predictions['memory_usage'], 2),
        'predicted_disk_usage': round(predictions['disk_usage'], 2),
        
        # AI recommendations
        'ai_recommendations': recommendations,
        
        # Action variables
        **ansible_vars
    }
    
    # Save as YAML file
    with open('ai_vars.yml', 'w') as f:
        yaml.dump(vars_dict, f, default_flow_style=False, indent=2)
    
    print("AI configuration converted to Ansible variables (ai_vars.yml)")
    return True

if __name__ == "__main__":
    convert_ai_config_to_ansible_vars()
Run the conversion script:
python3 convert_ai_to_ansible.py
Verify the generated Ansible variables:
cat ai_vars.yml
Subtask 3.2: Execute AI-Optimized Automation

Run the AI-enhanced Ansible playbook:
ansible-playbook ai-optimized-playbook.yml
Check the generated optimization report:
ls -la optimization_report_*.txt
cat optimization_report_*.txt
Subtask 3.3: Create a Comprehensive Automation Script

Create an integrated automation script:
nano ai_ansible_automation.py
Add the comprehensive automation script:
#!/usr/bin/env python3
import subprocess
import json
import time
import os
from datetime import datetime

class AIAnsibleAutomation:
    def __init__(self):
        self.log_file = f"automation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    def log_message(self, message):
        """Log messages to file and console"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        with open(self.log_file, 'a') as f:
            f.write(log_entry + '\n')
    
    def run_command(self, command, description):
        """Run a command and log the results"""
        self.log_message(f"Starting: {description}")
        self.log_message(f"Command: {command}")
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
            if result.returncode == 0:
                self.log_message(f"Success: {description}")
                if result.stdout:
                    self.log_message(f"Output: {result.stdout.strip()}")
                return True
            else:
                self.log_message(f"Error: {description}")
                self.log_message(f"Error output: {result.stderr.strip()}")
                return False
                
        except subprocess.TimeoutExpired:
            self.log_message(f"Timeout: {description}")
            return False
        except Exception as e:
            self.log_message(f"Exception: {description} - {str(e)}")
            return False
    
    def simulate_system_monitoring(self):
        """Simulate getting current system metrics"""
        self.log_message("Simulating system monitoring data collection...")
        
        # In a real scenario, this would collect actual system metrics
        import random
        current_metrics = {
            'cpu_usage': round(random.uniform(30, 90), 2),
            'memory_usage': round(random.uniform(40, 85), 2),
            'disk_usage': round(random.uniform(50, 95), 2),
            'timestamp': datetime.now().isoformat()
        }
        
        with open('current_metrics.json', 'w') as f:
            json.dump(current_metrics, f, indent=2)
        
        self.log_message(f"Current metrics: {current_metrics}")
        return current_metrics
    
    def run_full_automation_cycle(self):
        """Run the complete AI-driven automation cycle"""
        self.log_message("=== Starting AI-Driven Ansible Automation Cycle ===")
        
        # Step 1: Generate training data
        if not self.run_command(
            "python3 generate_system_data.py",
            "Generating system monitoring data"
        ):
            return False
        
        # Step 2: Run ML predictions
        if not self.run_command(
            "python3 ml_system_predictor.py",
            "Running machine learning predictions"
        ):
            return False
        
        # Step 3: Convert AI config to Ansible vars
        if not self.run_command(
            "python3 convert_ai_to_ansible.py",
            "Converting AI configuration to Ansible variables"
        ):
            return False
        
        # Step 4: Execute Ansible playbook
        if not self.run_command(
            "ansible-playbook ai-optimized-playbook.yml",
            "Executing AI-optimized Ansible playbook"
        ):
            return False
        
        # Step 5: Generate summary report
        self.generate_summary_report()
        
        self.log_message("=== AI-Driven Automation Cycle Complete ===")
        return True
    
    def generate_summary_report(self):
        """Generate a comprehensive summary report"""
        self.log_message("Generating comprehensive summary report...")
        
        report_content = f"""
AI-Driven Ansible Automation Summary Report
==========================================
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Automation Cycle Results:
- System data generation: Completed
- Machine learning predictions: Completed
- Ansible variable conversion: Completed
- Playbook execution: Completed

Files Generated:
- system_monitoring_data.csv: Historical system data
- trained_models.pkl: Machine learning models
- ai_ansible_config.json: AI-generated configuration
- ai_vars.yml: Ansible variables
- optimization_report_*.txt: Execution report
- {self.log_file}: Automation log

Next Steps:
1. Review the optimization recommendations
2. Monitor system performance after changes
3. Retrain models with new data periodically
4. Adjust thresholds based on business requirements

This automation cycle demonstrates how AI can enhance
infrastructure management by predicting resource needs
and automatically adjusting configurations.
"""
        
        with open('automation_summary.txt', 'w') as f:
            f.write(report_content)
        
        self.log_message("Summary report saved to automation_summary.txt")

def main():
    automation = AIAnsibleAutomation()
    
    print("AI-Driven Ansible Automation System")
    print("===================================")
    
    success = automation.run_full_automation_cycle()
    
    if success:
        print(f"\nAutomation completed successfully!")
        print(f"Check {automation.log_file} for detailed logs")
        print("Review automation_summary.txt for a complete summary")
    else:
        print(f"\nAutomation encountered errors.")
        print(f"Check {automation.log_file} for details")

if __name__ == "__main__":
    main()
Make the script executable and run it:
chmod +x ai_ansible_automation.py
python3 ai_ansible_automation.py
Review all generated files:
ls -la *.txt *.json *.yml *.csv *.pkl
Examine the comprehensive summary:
cat automation_summary.txt
Task 4: Advanced AI Integration and Monitoring

Subtask 4.1: Create a Monitoring Dashboard Script

Create a simple monitoring dashboard:
nano monitoring_dashboard.py
Add the dashboard script:
#!/usr/bin/env python3
import json
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import os

def create_monitoring_dashboard():
    """Create a simple text-based monitoring dashboard"""
    
    print("=" * 60)
    print("AI-DRIVEN ANSIBLE MONITORING DASHBOARD")
    print("=" * 60)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Load and display current predictions
    try:
        with open('ai_ansible_config.json', 'r') as f:
            config = json.load(f)
        
        print("CURRENT AI PREDICTIONS:")
        print("-" * 30)
        predictions = config['predicted_metrics']
        for metric, value in predictions.items():
            status = "🔴 HIGH" if value > 80 else "🟡 MEDIUM" if value > 60 else "🟢 LOW"
            print(f"{metric.replace('_', ' ').title()}: {value:.1f}% {status}")
        
        print("\nAI RECOMMENDATIONS:")
        print("-" * 30)
        for i, rec in enumerate(config['recommendations'], 1):
            print(f"{i}. {rec}")
        
    except FileNotFoundError:
        print("No AI configuration found. Run the predictor first.")
    
    # Load and display historical trends
    try:
        df = pd.read_csv('system_monitoring_data.csv')
        
        print(f"\nHISTORICAL DATA SUMMARY:")
        print("-" * 30)
        print(f"Total data points: {len(df)}")
        print(f"Date range: {df['timestamp'].min()} to {df['timestamp'].max()}")
        
        # Calculate averages
        avg_cpu = df['cpu_usage'].mean()
        avg_memory = df['memory_usage'].mean()
        avg_disk = df['disk_usage'].mean()
        
        print(f"\nAVERAGE RESOURCE USAGE:")
        print(f"CPU: {avg_cpu:.1f}%")
        print(f"Memory: {avg_memory:.1f}%")
        print(f"Disk: {avg_disk:.1f}%")
        
    except FileNotFoundError:
        print("No historical data found.")
    
    # Display recent automation activities
    print(f"\nRECENT AUTOMATION ACTIVITIES:")
    print("-" * 30)
    
    log_files = [f for f in os.listdir('.') if f.startswith('automation_log_')]
    if log_files:
        latest_log = sorted(log_files)[-1]
        print(f"Latest log: {latest_log}")
        
        with open(latest_log, 'r') as f:
            lines = f.readlines()
            print("Last 5 activities:")
            for line in lines[-5:]:
                print(f"  {line.strip()}")
    else:
        print("No automation logs found.")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    create_monitoring_dashboard()
Run the monitoring dashboard:
python3 monitoring_dashboard.py
Subtask 4.2: Create a Continuous Monitoring Script

Create a continuous monitoring script:
nano continuous_monitor.py
Add the continuous monitoring script:
#!/usr/bin/env python3
import time
import json
import subprocess
from datetime import datetime
import signal
import sys

class ContinuousMonitor:
    def __init__(self, interval=300):  # 5 minutes default
        self.interval = interval
        self.running = True
        self.cycle_count = 0
        
        # Handle Ctrl+C gracefully
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        print(f"\nReceived interrupt signal. Stopping monitor...")
        self.running = False
    
    def log_message(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)
        
        with open('continuous_monitor.log', 'a') as f:
            f.write(log_entry + '\n')
    
    def run_prediction_cycle(self):
        """Run a single prediction and optimization cycle"""
        self.cycle_count += 1
        self.log_message(f"Starting monitoring cycle #{self
