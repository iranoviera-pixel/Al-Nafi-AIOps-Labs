Lab 60: AI-Driven Predictive Monitoring and Performance Optimization

Objectives

By the end of this lab, students will be able to:

Understand the fundamentals of AI-driven predictive monitoring systems
Research and evaluate open-source AI-based monitoring tools
Implement machine learning algorithms to predict system performance bottlenecks
Create predictive maintenance workflows based on AI insights
Build a complete monitoring solution using Python and open-source libraries
Analyze system metrics and generate actionable performance recommendations
Prerequisites

Before starting this lab, students should have:

Basic understanding of Linux command line operations
Fundamental knowledge of Python programming
Basic concepts of system monitoring (CPU, memory, disk usage)
Understanding of machine learning concepts (regression, classification)
Familiarity with data analysis and visualization
Required Knowledge Level: Beginner-friendly with step-by-step guidance

Lab Environment Setup

Al Nafi Cloud Machine: This lab uses Al Nafi's pre-configured Linux-based cloud machines. Simply click Start Lab to access your ready-to-use environment. No need to build or configure your own virtual machine.

Pre-installed Tools: Your cloud machine comes with Python 3, pip, and essential development tools already configured.

Task 1: Research AI-Based Predictive Monitoring Tools

Subtask 1.1: Understanding Predictive Monitoring

What is Predictive Monitoring?

Predictive monitoring uses artificial intelligence and machine learning to analyze historical system data and predict future performance issues before they occur. This proactive approach helps prevent system failures and optimize resource utilization.

Subtask 1.2: Exploring Open-Source AI Monitoring Tools

Let's research and understand popular open-source tools:

Access your cloud machine terminal

Create a research directory:

mkdir ~/ai-monitoring-lab
cd ~/ai-monitoring-lab
Create a research document:
nano monitoring-tools-research.md
Add the following research content:
# AI-Based Predictive Monitoring Tools Research

## 1. Prometheus + Grafana + Machine Learning
- **Purpose**: Time-series monitoring with ML capabilities
- **Strengths**: Excellent for metrics collection and visualization
- **Use Case**: Real-time monitoring with predictive alerts

## 2. Scikit-learn for Predictive Analytics
- **Purpose**: Machine learning library for Python
- **Strengths**: Easy-to-use ML algorithms
- **Use Case**: Building custom prediction models

## 3. Pandas + NumPy for Data Processing
- **Purpose**: Data manipulation and analysis
- **Strengths**: Powerful data processing capabilities
- **Use Case**: Preparing system metrics for ML analysis

## 4. Matplotlib + Seaborn for Visualization
- **Purpose**: Data visualization libraries
- **Strengths**: Create insightful charts and graphs
- **Use Case**: Visualizing predictions and system trends
Save and exit (Ctrl+X, then Y, then Enter)
Subtask 1.3: Installing Required Libraries

Install the necessary Python libraries for our AI monitoring solution:

# Update system packages
sudo apt update

# Install Python development tools
sudo apt install -y python3-pip python3-dev python3-venv

# Create virtual environment
python3 -m venv ai-monitoring-env
source ai-monitoring-env/bin/activate

# Install required libraries
pip install pandas numpy scikit-learn matplotlib seaborn psutil schedule requests
Task 2: Write Python Script for Performance Prediction

Subtask 2.1: Create System Metrics Collection Script

Create a script to collect system performance data:

nano system_metrics_collector.py
Add the following code:

#!/usr/bin/env python3
"""
System Metrics Collector for AI-Driven Predictive Monitoring
Collects CPU, memory, disk, and network metrics for analysis
"""

import psutil
import time
import json
import datetime
import os

class SystemMetricsCollector:
    def __init__(self, output_file="system_metrics.json"):
        self.output_file = output_file
        self.metrics_data = []
    
    def collect_cpu_metrics(self):
        """Collect CPU usage metrics"""
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq()
        
        return {
            'cpu_percent': cpu_percent,
            'cpu_count': cpu_count,
            'cpu_freq_current': cpu_freq.current if cpu_freq else 0,
            'cpu_freq_max': cpu_freq.max if cpu_freq else 0
        }
    
    def collect_memory_metrics(self):
        """Collect memory usage metrics"""
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        return {
            'memory_total': memory.total,
            'memory_available': memory.available,
            'memory_percent': memory.percent,
            'memory_used': memory.used,
            'swap_total': swap.total,
            'swap_used': swap.used,
            'swap_percent': swap.percent
        }
    
    def collect_disk_metrics(self):
        """Collect disk usage metrics"""
        disk_usage = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        
        return {
            'disk_total': disk_usage.total,
            'disk_used': disk_usage.used,
            'disk_free': disk_usage.free,
            'disk_percent': disk_usage.used / disk_usage.total * 100,
            'disk_read_bytes': disk_io.read_bytes if disk_io else 0,
            'disk_write_bytes': disk_io.write_bytes if disk_io else 0
        }
    
    def collect_network_metrics(self):
        """Collect network usage metrics"""
        net_io = psutil.net_io_counters()
        
        return {
            'bytes_sent': net_io.bytes_sent,
            'bytes_recv': net_io.bytes_recv,
            'packets_sent': net_io.packets_sent,
            'packets_recv': net_io.packets_recv
        }
    
    def collect_all_metrics(self):
        """Collect all system metrics"""
        timestamp = datetime.datetime.now().isoformat()
        
        metrics = {
            'timestamp': timestamp,
            'cpu': self.collect_cpu_metrics(),
            'memory': self.collect_memory_metrics(),
            'disk': self.collect_disk_metrics(),
            'network': self.collect_network_metrics()
        }
        
        return metrics
    
    def save_metrics(self, metrics):
        """Save metrics to JSON file"""
        self.metrics_data.append(metrics)
        
        with open(self.output_file, 'w') as f:
            json.dump(self.metrics_data, f, indent=2)
    
    def run_collection(self, duration_minutes=10, interval_seconds=30):
        """Run metrics collection for specified duration"""
        print(f"Starting metrics collection for {duration_minutes} minutes...")
        print(f"Collecting data every {interval_seconds} seconds")
        
        end_time = time.time() + (duration_minutes * 60)
        
        while time.time() < end_time:
            try:
                metrics = self.collect_all_metrics()
                self.save_metrics(metrics)
                
                print(f"Collected metrics at {metrics['timestamp']}")
                print(f"  CPU: {metrics['cpu']['cpu_percent']:.1f}%")
                print(f"  Memory: {metrics['memory']['memory_percent']:.1f}%")
                print(f"  Disk: {metrics['disk']['disk_percent']:.1f}%")
                print("-" * 50)
                
                time.sleep(interval_seconds)
                
            except KeyboardInterrupt:
                print("\nCollection stopped by user")
                break
            except Exception as e:
                print(f"Error collecting metrics: {e}")
                time.sleep(interval_seconds)
        
        print(f"Metrics collection completed. Data saved to {self.output_file}")

if __name__ == "__main__":
    collector = SystemMetricsCollector()
    collector.run_collection(duration_minutes=5, interval_seconds=10)
Subtask 2.2: Create Machine Learning Prediction Script

Create the main prediction script:

nano ai_performance_predictor.py
Add the following comprehensive code:

#!/usr/bin/env python3
"""
AI-Driven Performance Predictor
Uses machine learning to predict system performance bottlenecks
"""

import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class AIPerformancePredictor:
    def __init__(self, data_file="system_metrics.json"):
        self.data_file = data_file
        self.df = None
        self.scaler = StandardScaler()
        self.cpu_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.memory_model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.bottleneck_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def load_and_prepare_data(self):
        """Load and prepare data for machine learning"""
        print("Loading system metrics data...")
        
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Data file {self.data_file} not found. Please run metrics collection first.")
            return False
        
        # Convert to DataFrame
        rows = []
        for entry in data:
            row = {
                'timestamp': entry['timestamp'],
                'cpu_percent': entry['cpu']['cpu_percent'],
                'cpu_count': entry['cpu']['cpu_count'],
                'memory_percent': entry['memory']['memory_percent'],
                'memory_used': entry['memory']['memory_used'],
                'memory_total': entry['memory']['memory_total'],
                'disk_percent': entry['disk']['disk_percent'],
                'disk_used': entry['disk']['disk_used'],
                'bytes_sent': entry['network']['bytes_sent'],
                'bytes_recv': entry['network']['bytes_recv']
            }
            rows.append(row)
        
        self.df = pd.DataFrame(rows)
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
        
        # Create time-based features
        self.df['hour'] = self.df['timestamp'].dt.hour
        self.df['minute'] = self.df['timestamp'].dt.minute
        self.df['day_of_week'] = self.df['timestamp'].dt.dayofweek
        
        # Create lag features (previous values)
        self.df['cpu_lag1'] = self.df['cpu_percent'].shift(1)
        self.df['memory_lag1'] = self.df['memory_percent'].shift(1)
        
        # Create moving averages
        self.df['cpu_ma3'] = self.df['cpu_percent'].rolling(window=3).mean()
        self.df['memory_ma3'] = self.df['memory_percent'].rolling(window=3).mean()
        
        # Create bottleneck labels
        self.df['cpu_bottleneck'] = (self.df['cpu_percent'] > 80).astype(int)
        self.df['memory_bottleneck'] = (self.df['memory_percent'] > 85).astype(int)
        self.df['disk_bottleneck'] = (self.df['disk_percent'] > 90).astype(int)
        
        # Overall bottleneck (any resource above threshold)
        self.df['bottleneck'] = ((self.df['cpu_bottleneck'] == 1) | 
                                (self.df['memory_bottleneck'] == 1) | 
                                (self.df['disk_bottleneck'] == 1)).astype(int)
        
        # Remove rows with NaN values
        self.df = self.df.dropna()
        
        print(f"Loaded {len(self.df)} data points")
        return True
    
    def create_features(self):
        """Create feature matrix for machine learning"""
        feature_columns = [
            'cpu_percent', 'memory_percent', 'disk_percent',
            'hour', 'minute', 'day_of_week',
            'cpu_lag1', 'memory_lag1',
            'cpu_ma3', 'memory_ma3'
        ]
        
        return self.df[feature_columns].values
    
    def train_prediction_models(self):
        """Train machine learning models for performance prediction"""
        print("Training AI prediction models...")
        
        X = self.create_features()
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train CPU prediction model
        y_cpu = self.df['cpu_percent'].values
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_cpu, test_size=0.2, random_state=42
        )
        
        self.cpu_model.fit(X_train, y_train)
        cpu_predictions = self.cpu_model.predict(X_test)
        cpu_mse = mean_squared_error(y_test, cpu_predictions)
        
        print(f"CPU Prediction Model - MSE: {cpu_mse:.2f}")
        
        # Train Memory prediction model
        y_memory = self.df['memory_percent'].values
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_memory, test_size=0.2, random_state=42
        )
        
        self.memory_model.fit(X_train, y_train)
        memory_predictions = self.memory_model.predict(X_test)
        memory_mse = mean_squared_error(y_test, memory_predictions)
        
        print(f"Memory Prediction Model - MSE: {memory_mse:.2f}")
        
        # Train Bottleneck Classification Model
        y_bottleneck = self.df['bottleneck'].values
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y_bottleneck, test_size=0.2, random_state=42
        )
        
        self.bottleneck_classifier.fit(X_train, y_train)
        bottleneck_predictions = self.bottleneck_classifier.predict(X_test)
        bottleneck_accuracy = accuracy_score(y_test, bottleneck_predictions)
        
        print(f"Bottleneck Classification Model - Accuracy: {bottleneck_accuracy:.2f}")
        
        return True
    
    def predict_future_performance(self, hours_ahead=1):
        """Predict future system performance"""
        print(f"Predicting system performance {hours_ahead} hours ahead...")
        
        # Get latest data point
        latest_data = self.df.iloc[-1]
        
        # Create feature vector for prediction
        features = np.array([[
            latest_data['cpu_percent'],
            latest_data['memory_percent'],
            latest_data['disk_percent'],
            (latest_data['hour'] + hours_ahead) % 24,
            latest_data['minute'],
            latest_data['day_of_week'],
            latest_data['cpu_lag1'],
            latest_data['memory_lag1'],
            latest_data['cpu_ma3'],
            latest_data['memory_ma3']
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Make predictions
        cpu_prediction = self.cpu_model.predict(features_scaled)[0]
        memory_prediction = self.memory_model.predict(features_scaled)[0]
        bottleneck_probability = self.bottleneck_classifier.predict_proba(features_scaled)[0][1]
        
        predictions = {
            'predicted_cpu_percent': cpu_prediction,
            'predicted_memory_percent': memory_prediction,
            'bottleneck_probability': bottleneck_probability,
            'prediction_time': datetime.now() + timedelta(hours=hours_ahead)
        }
        
        return predictions
    
    def generate_recommendations(self, predictions):
        """Generate performance optimization recommendations"""
        recommendations = []
        
        if predictions['predicted_cpu_percent'] > 80:
            recommendations.append({
                'type': 'CPU Warning',
                'message': f"High CPU usage predicted: {predictions['predicted_cpu_percent']:.1f}%",
                'action': 'Consider scaling CPU resources or optimizing CPU-intensive processes'
            })
        
        if predictions['predicted_memory_percent'] > 85:
            recommendations.append({
                'type': 'Memory Warning',
                'message': f"High memory usage predicted: {predictions['predicted_memory_percent']:.1f}%",
                'action': 'Consider increasing memory or optimizing memory usage'
            })
        
        if predictions['bottleneck_probability'] > 0.7:
            recommendations.append({
                'type': 'Bottleneck Alert',
                'message': f"High bottleneck probability: {predictions['bottleneck_probability']:.2f}",
                'action': 'Proactive resource scaling recommended'
            })
        
        if not recommendations:
            recommendations.append({
                'type': 'System Healthy',
                'message': 'No performance issues predicted',
                'action': 'Continue monitoring'
            })
        
        return recommendations
    
    def visualize_predictions(self):
        """Create visualizations of system performance and predictions"""
        print("Creating performance visualizations...")
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('AI-Driven System Performance Analysis', fontsize=16)
        
        # CPU Usage Over Time
        axes[0, 0].plot(self.df['timestamp'], self.df['cpu_percent'], 'b-', alpha=0.7)
        axes[0, 0].axhline(y=80, color='r', linestyle='--', label='Warning Threshold')
        axes[0, 0].set_title('CPU Usage Over Time')
        axes[0, 0].set_ylabel('CPU %')
        axes[0, 0].legend()
        axes[0, 0].tick_params(axis='x', rotation=45)
        
        # Memory Usage Over Time
        axes[0, 1].plot(self.df['timestamp'], self.df['memory_percent'], 'g-', alpha=0.7)
        axes[0, 1].axhline(y=85, color='r', linestyle='--', label='Warning Threshold')
        axes[0, 1].set_title('Memory Usage Over Time')
        axes[0, 1].set_ylabel('Memory %')
        axes[0, 1].legend()
        axes[0, 1].tick_params(axis='x', rotation=45)
        
        # Resource Usage Distribution
        axes[1, 0].hist(self.df['cpu_percent'], bins=20, alpha=0.7, label='CPU', color='blue')
        axes[1, 0].hist(self.df['memory_percent'], bins=20, alpha=0.7, label='Memory', color='green')
        axes[1, 0].set_title('Resource Usage Distribution')
        axes[1, 0].set_xlabel('Usage %')
        axes[1, 0].set_ylabel('Frequency')
        axes[1, 0].legend()
        
        # Bottleneck Prediction
        bottleneck_counts = self.df['bottleneck'].value_counts()
        axes[1, 1].pie(bottleneck_counts.values, labels=['Normal', 'Bottleneck'], 
                      autopct='%1.1f%%', startangle=90)
        axes[1, 1].set_title('Bottleneck Distribution')
        
        plt.tight_layout()
        plt.savefig('performance_analysis.png', dpi=300, bbox_inches='tight')
        print("Visualization saved as 'performance_analysis.png'")
        
        return True
    
    def run_complete_analysis(self):
        """Run complete AI-driven performance analysis"""
        print("=" * 60)
        print("AI-DRIVEN PREDICTIVE MONITORING AND OPTIMIZATION")
        print("=" * 60)
        
        # Load and prepare data
        if not self.load_and_prepare_data():
            return False
        
        # Train models
        self.train_prediction_models()
        
        # Make predictions
        predictions_1h = self.predict_future_performance(hours_ahead=1)
        predictions_4h = self.predict_future_performance(hours_ahead=4)
        
        # Generate recommendations
        recommendations_1h = self.generate_recommendations(predictions_1h)
        recommendations_4h = self.generate_recommendations(predictions_4h)
        
        # Display results
        print("\n" + "=" * 40)
        print("PERFORMANCE PREDICTIONS")
        print("=" * 40)
        
        print(f"\n1-Hour Ahead Predictions:")
        print(f"  CPU Usage: {predictions_1h['predicted_cpu_percent']:.1f}%")
        print(f"  Memory Usage: {predictions_1h['predicted_memory_percent']:.1f}%")
        print(f"  Bottleneck Probability: {predictions_1h['bottleneck_probability']:.2f}")
        
        print(f"\n4-Hour Ahead Predictions:")
        print(f"  CPU Usage: {predictions_4h['predicted_cpu_percent']:.1f}%")
        print(f"  Memory Usage: {predictions_4h['predicted_memory_percent']:.1f}%")
        print(f"  Bottleneck Probability: {predictions_4h['bottleneck_probability']:.2f}")
        
        print("\n" + "=" * 40)
        print("RECOMMENDATIONS")
        print("=" * 40)
        
        print("\n1-Hour Recommendations:")
        for rec in recommendations_1h:
            print(f"  [{rec['type']}] {rec['message']}")
            print(f"    Action: {rec['action']}")
        
        print("\n4-Hour Recommendations:")
        for rec in recommendations_4h:
            print(f"  [{rec['type']}] {rec['message']}")
            print(f"    Action: {rec['action']}")
        
        # Create visualizations
        self.visualize_predictions()
        
        return True

if __name__ == "__main__":
    predictor = AIPerformancePredictor()
    predictor.run_complete_analysis()
Subtask 2.3: Test the Prediction System

First, collect system metrics:
python3 system_metrics_collector.py
Run the AI prediction analysis:
python3 ai_performance_predictor.py
View the generated visualization:
ls -la *.png
Task 3: Implement Predictive Maintenance

Subtask 3.1: Create Automated Monitoring Script

Create a script that continuously monitors and takes action:

nano predictive_maintenance.py
Add the following code:

#!/usr/bin/env python3
"""
Predictive Maintenance System
Automatically monitors system and takes preventive actions
"""

import time
import json
import subprocess
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import psutil
import schedule
from ai_performance_predictor import AIPerformancePredictor
from system_metrics_collector import SystemMetricsCollector

class PredictiveMaintenanceSystem:
    def __init__(self):
        self.collector = SystemMetricsCollector("maintenance_metrics.json")
        self.predictor = AIPerformancePredictor("maintenance_metrics.json")
        self.alert_log = "maintenance_alerts.log"
        self.maintenance_actions = []
    
    def log_alert(self, message):
        """Log maintenance alerts"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        with open(self.alert_log, 'a') as f:
            f.write(log_entry)
        
        print(f"ALERT: {message}")
    
    def check_disk_space(self):
        """Check and clean disk space if needed"""
        disk_usage = psutil.disk_usage('/')
        disk_percent = (disk_usage.used / disk_usage.total) * 100
        
        if disk_percent > 85:
            self.log_alert(f"High disk usage detected: {disk_percent:.1f}%")
            
            # Attempt to clean temporary files
            try:
                subprocess.run(['sudo', 'apt', 'autoremove', '-y'], 
                             capture_output=True, text=True)
                subprocess.run(['sudo', 'apt', 'autoclean'], 
                             capture_output=True, text=True)
                
                # Clean temporary directories
                subprocess.run(['sudo', 'rm', '-rf', '/tmp/*'], 
                             capture_output=True, text=True)
                
                self.log_alert("Automatic disk cleanup completed")
                
            except Exception as e:
                self.log_alert(f"Disk cleanup failed: {e}")
    
    def optimize_memory(self):
        """Optimize memory usage"""
        memory = psutil.virtual_memory()
        
        if memory.percent > 85:
            self.log_alert(f"High memory usage detected: {memory.percent:.1f}%")
            
            try:
                # Clear system caches
                subprocess.run(['sudo', 'sync'], capture_output=True)
                subprocess.run(['sudo', 'sysctl', 'vm.drop_caches=3'], 
                             capture_output=True)
                
                self.log_alert("Memory optimization completed")
                
            except Exception as e:
                self.log_alert(f"Memory optimization failed: {e}")
    
    def restart_high_cpu_processes(self):
        """Identify and manage high CPU processes"""
        cpu_percent = psutil.cpu_percent(interval=1)
        
        if cpu_percent > 80:
            self.log_alert(f"High CPU usage detected: {cpu_percent:.1f}%")
            
            # Get top CPU processes
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    proc_info = proc.info
                    if proc_info['cpu_percent'] > 10:
                        processes.append(proc_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            # Sort by CPU usage
            processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
            
            if processes:
                self.log_alert(f"Top CPU processes: {processes[:3]}")
    
    def generate_maintenance_report(self):
        """Generate comprehensive maintenance report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'system_status': {},
            'predictions': {},
            'actions_taken': self.maintenance_actions.copy()
        }
        
        # Current system status
        report['system_status'] = {
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': (psutil.disk_usage('/').used / 
                           psutil.disk_usage('/').total) * 100
        }
        
        # Save report
        with open('maintenance_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log_alert("Maintenance report generated")
        
        return report
    
    def run_predictive_analysis(self):
        """Run AI-based predictive analysis"""
        try:
            # Collect current metrics
            metrics = self.collector.collect_all_metrics()
            self.collector.save_metrics(metrics)
            
            # Check if we have enough data for prediction
            try:
                with open("maintenance_metrics.json", 'r') as f:
                    data = json.load(f)
                    
                if len(data) >= 10:  # Need minimum data points
                    # Load data and make predictions
                    if self.predictor.load_and_prepare_data():
                        self.predictor.train_prediction_models()
                        
                        predictions = self.predictor.predict_future_performance(hours_ahead=1)
                        recommendations = self.predictor.generate_recommendations(predictions)
                        
                        # Act on recommendations
                        for rec in recommendations:
                            if rec['type'] in ['CPU Warning', 'Memory Warning', 'Bottleneck Alert']:
                                self.log_alert(f"Predictive Alert: {rec['message']}")
                                self.maintenance_actions.append({
                                    'timestamp': datetime.now().isoformat(),
                                    'type': 'predictive_action',
                                    'recommendation': rec
                                })
                
            except FileNotFoundError:
                self.log_alert("Insufficient data for predictions, continuing monitoring...")
                
        except Exception as e:
            self.log_alert(f"Predictive analysis error: {e}")
    
    def run_maintenance_cycle(self):
        """Run complete maintenance cycle"""
        self.log_alert("Starting maintenance cycle")
        
        # Collect metrics and run predictions
        self.run_predictive_analysis()
        
        # Perform maintenance checks
        self.check_disk_space()
        self.optimize_memory()
        self.restart_high_cpu_processes()
        
        # Generate report
        self.generate_maintenance_report()
        
        self.log_alert("Maintenance cycle completed")
    
    def start_continuous_monitoring(self):
        """Start continuous predictive monitoring"""
        print("Starting Predictive Maintenance System...")
        print("Press Ctrl+C to stop")
        
        # Schedule maintenance tasks
        schedule.every(5).minutes.do(self.run_maintenance_cycle)
        schedule.every(1).hours.do(self.generate_maintenance_report)
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
        except KeyboardInterrupt:
            print("\nPredictive Maintenance System stopped")
            self.log_alert("Predictive Maintenance System stopped by user")

if __name__ == "__main__":
    maintenance_system = PredictiveMaintenanceSystem()
    maintenance_system.start_continuous_monitoring()
Subtask 3.2: Create System Health Dashboard

Create a simple web dashboard to view system health:

nano health_dashboard.py
Add the following code:

#!/usr/bin/env python3
"""
Simple System Health Dashboard
Displays current system status and predictions
"""

import json
import psutil
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.animation import FuncAnimation
import pandas as pd

class HealthDashboard:
    def __init__(self):
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle('System Health Dashboard', fontsize=16)
        
    def get_current_status(self):
        """Get current system status"""
        return {
            'timestamp': datetime.now(),
            'cpu_percent': psutil.cpu_percent(),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_percent': (psutil.disk_usage('/').used / 
                           psutil.disk_usage('/').total) * 100,
            'network
