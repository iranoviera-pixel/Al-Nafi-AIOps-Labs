Lab 30: AI-Driven Storage Optimization and Monitoring

Objectives

By the end of this lab, students will be able to:

Understand the fundamentals of AI-driven storage optimization techniques
Research and identify open-source AI tools suitable for storage management
Develop Python scripts using machine learning algorithms to predict storage needs
Implement automated storage optimization based on usage patterns
Create AI-based monitoring systems for storage performance
Analyze storage metrics and generate predictive insights
Configure automated alerts and optimization triggers
Prerequisites

Before starting this lab, students should have:

Basic understanding of Linux command line operations
Fundamental knowledge of Python programming
Basic concepts of machine learning and data analysis
Understanding of storage systems and file management
Familiarity with system monitoring concepts
Required Knowledge Level: Beginner-friendly with step-by-step guidance

Lab Environment Setup

Good News: Al Nafi provides ready-to-use Linux-based cloud machines for this lab. Simply click Start Lab and you'll have access to a fully configured environment with all necessary tools pre-installed. No need to build your own virtual machine or install software packages.

Your cloud machine includes:

Ubuntu 22.04 LTS
Python 3.10 with pip
Essential development tools
Storage monitoring utilities
Sample datasets for training
Task 1: Research AI Tools for Storage Optimization

Subtask 1.1: Understanding AI-Driven Storage Optimization

AI-driven storage optimization uses machine learning algorithms to:

Predict future storage requirements
Optimize data placement and access patterns
Automate storage provisioning and deprovisioning
Identify storage bottlenecks and performance issues
Implement intelligent data tiering strategies
Subtask 1.2: Exploring Open-Source AI Tools

Let's research and explore popular open-source tools for storage optimization:

# Update system packages
sudo apt update && sudo apt upgrade -y

# Install research and documentation tools
sudo apt install -y curl wget tree htop iotop
Key Open-Source Tools for Storage AI:

Scikit-learn: Machine learning library for predictive analytics
Pandas: Data manipulation and analysis
NumPy: Numerical computing for data processing
Matplotlib/Seaborn: Data visualization
Prometheus: Monitoring and alerting toolkit
Grafana: Analytics and monitoring platform
Subtask 1.3: Installing Required Python Libraries

# Install Python package manager and virtual environment
sudo apt install -y python3-pip python3-venv

# Create a virtual environment for our project
python3 -m venv storage_ai_env

# Activate the virtual environment
source storage_ai_env/bin/activate

# Install required Python libraries
pip install scikit-learn pandas numpy matplotlib seaborn psutil
pip install prometheus-client grafana-api requests
Subtask 1.4: Setting Up Project Structure

# Create project directory structure
mkdir -p ~/storage_ai_lab/{scripts,data,models,logs,config}
cd ~/storage_ai_lab

# Create initial project files
touch scripts/storage_predictor.py
touch scripts/storage_monitor.py
touch scripts/data_collector.py
touch config/settings.py
Task 2: Write Python Script for Storage Prediction and Optimization

Subtask 2.1: Creating Data Collection Script

First, let's create a script to collect storage usage data:

# File: scripts/data_collector.py
import psutil
import pandas as pd
import json
import time
from datetime import datetime
import os

class StorageDataCollector:
    def __init__(self, data_file="data/storage_metrics.csv"):
        self.data_file = data_file
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
    
    def collect_storage_metrics(self):
        """Collect current storage metrics"""
        metrics = {
            'timestamp': datetime.now().isoformat(),
            'total_space': 0,
            'used_space': 0,
            'free_space': 0,
            'usage_percent': 0,
            'read_count': 0,
            'write_count': 0,
            'read_bytes': 0,
            'write_bytes': 0
        }
        
        # Get disk usage statistics
        disk_usage = psutil.disk_usage('/')
        metrics['total_space'] = disk_usage.total
        metrics['used_space'] = disk_usage.used
        metrics['free_space'] = disk_usage.free
        metrics['usage_percent'] = (disk_usage.used / disk_usage.total) * 100
        
        # Get disk I/O statistics
        disk_io = psutil.disk_io_counters()
        if disk_io:
            metrics['read_count'] = disk_io.read_count
            metrics['write_count'] = disk_io.write_count
            metrics['read_bytes'] = disk_io.read_bytes
            metrics['write_bytes'] = disk_io.write_bytes
        
        return metrics
    
    def save_metrics(self, metrics):
        """Save metrics to CSV file"""
        df = pd.DataFrame([metrics])
        
        # Append to existing file or create new one
        if os.path.exists(self.data_file):
            df.to_csv(self.data_file, mode='a', header=False, index=False)
        else:
            df.to_csv(self.data_file, index=False)
    
    def collect_continuous(self, duration_minutes=60, interval_seconds=30):
        """Collect data continuously for specified duration"""
        print(f"Starting data collection for {duration_minutes} minutes...")
        end_time = time.time() + (duration_minutes * 60)
        
        while time.time() < end_time:
            metrics = self.collect_storage_metrics()
            self.save_metrics(metrics)
            print(f"Collected metrics at {metrics['timestamp']}")
            time.sleep(interval_seconds)
        
        print("Data collection completed!")

if __name__ == "__main__":
    collector = StorageDataCollector()
    
    # Collect sample data for 10 minutes (for demo purposes)
    collector.collect_continuous(duration_minutes=10, interval_seconds=10)
Subtask 2.2: Creating Storage Prediction Model

Now, let's create the main prediction script:

# File: scripts/storage_predictor.py
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import joblib
import os

class StoragePredictor:
    def __init__(self, data_file="data/storage_metrics.csv"):
        self.data_file = data_file
        self.model = None
        self.feature_columns = ['hour', 'day_of_week', 'usage_percent_lag1', 
                               'usage_percent_lag2', 'io_activity']
        
    def load_and_prepare_data(self):
        """Load and prepare data for machine learning"""
        if not os.path.exists(self.data_file):
            print("No data file found. Please run data collection first.")
            return None
        
        # Load data
        df = pd.read_csv(self.data_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Feature engineering
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        
        # Create lag features
        df['usage_percent_lag1'] = df['usage_percent'].shift(1)
        df['usage_percent_lag2'] = df['usage_percent'].shift(2)
        
        # Calculate I/O activity indicator
        df['io_activity'] = (df['read_bytes'] + df['write_bytes']) / 1024 / 1024  # MB
        
        # Remove rows with NaN values
        df = df.dropna()
        
        return df
    
    def train_model(self, df):
        """Train the storage prediction model"""
        if df is None or len(df) < 10:
            print("Insufficient data for training. Need at least 10 data points.")
            return False
        
        # Prepare features and target
        X = df[self.feature_columns]
        y = df['usage_percent']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest model
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model Performance:")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R² Score: {r2:.2f}")
        
        # Save model
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.model, "models/storage_predictor.pkl")
        
        return True
    
    def predict_future_usage(self, hours_ahead=24):
        """Predict storage usage for future hours"""
        if self.model is None:
            # Try to load existing model
            if os.path.exists("models/storage_predictor.pkl"):
                self.model = joblib.load("models/storage_predictor.pkl")
            else:
                print("No trained model found. Please train the model first.")
                return None
        
        # Load recent data for prediction
        df = self.load_and_prepare_data()
        if df is None or len(df) == 0:
            return None
        
        # Get the latest data point
        latest_data = df.iloc[-1]
        predictions = []
        
        # Predict for each hour ahead
        for hour in range(1, hours_ahead + 1):
            future_time = datetime.now() + timedelta(hours=hour)
            
            # Create feature vector
            features = np.array([[
                future_time.hour,
                future_time.weekday(),
                latest_data['usage_percent'],  # lag1
                df.iloc[-2]['usage_percent'] if len(df) > 1 else latest_data['usage_percent'],  # lag2
                latest_data['io_activity']
            ]])
            
            prediction = self.model.predict(features)[0]
            predictions.append({
                'timestamp': future_time,
                'predicted_usage': prediction
            })
        
        return predictions
    
    def optimize_storage(self, predictions):
        """Provide storage optimization recommendations"""
        if not predictions:
            return []
        
        recommendations = []
        
        for pred in predictions:
            usage = pred['predicted_usage']
            timestamp = pred['timestamp']
            
            if usage > 90:
                recommendations.append({
                    'timestamp': timestamp,
                    'severity': 'CRITICAL',
                    'message': f'Storage usage predicted to reach {usage:.1f}%. Immediate action required!',
                    'actions': [
                        'Clean temporary files',
                        'Archive old logs',
                        'Move large files to external storage',
                        'Consider adding more storage capacity'
                    ]
                })
            elif usage > 80:
                recommendations.append({
                    'timestamp': timestamp,
                    'severity': 'WARNING',
                    'message': f'Storage usage predicted to reach {usage:.1f}%. Plan optimization.',
                    'actions': [
                        'Review and clean unnecessary files',
                        'Compress large files',
                        'Schedule regular cleanup tasks'
                    ]
                })
            elif usage > 70:
                recommendations.append({
                    'timestamp': timestamp,
                    'severity': 'INFO',
                    'message': f'Storage usage predicted to reach {usage:.1f}%. Monitor closely.',
                    'actions': [
                        'Continue monitoring',
                        'Plan for future storage needs'
                    ]
                })
        
        return recommendations
    
    def visualize_predictions(self, predictions):
        """Create visualization of storage predictions"""
        if not predictions:
            print("No predictions to visualize.")
            return
        
        # Prepare data for plotting
        timestamps = [pred['timestamp'] for pred in predictions]
        usage_values = [pred['predicted_usage'] for pred in predictions]
        
        # Create plot
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, usage_values, marker='o', linewidth=2, markersize=6)
        plt.axhline(y=80, color='orange', linestyle='--', label='Warning Threshold (80%)')
        plt.axhline(y=90, color='red', linestyle='--', label='Critical Threshold (90%)')
        
        plt.title('Storage Usage Predictions', fontsize=16, fontweight='bold')
        plt.xlabel('Time', fontsize=12)
        plt.ylabel('Storage Usage (%)', fontsize=12)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save plot
        os.makedirs("logs", exist_ok=True)
        plt.savefig("logs/storage_predictions.png", dpi=300, bbox_inches='tight')
        plt.show()

def main():
    predictor = StoragePredictor()
    
    # Load and prepare data
    print("Loading and preparing data...")
    df = predictor.load_and_prepare_data()
    
    if df is not None:
        # Train model
        print("Training prediction model...")
        if predictor.train_model(df):
            # Make predictions
            print("Generating predictions for next 24 hours...")
            predictions = predictor.predict_future_usage(hours_ahead=24)
            
            if predictions:
                # Get optimization recommendations
                recommendations = predictor.optimize_storage(predictions)
                
                # Display results
                print("\n" + "="*50)
                print("STORAGE OPTIMIZATION RECOMMENDATIONS")
                print("="*50)
                
                for rec in recommendations:
                    print(f"\nTime: {rec['timestamp'].strftime('%Y-%m-%d %H:%M')}")
                    print(f"Severity: {rec['severity']}")
                    print(f"Message: {rec['message']}")
                    print("Recommended Actions:")
                    for action in rec['actions']:
                        print(f"  • {action}")
                
                # Create visualization
                predictor.visualize_predictions(predictions)
                
                print(f"\nPrediction visualization saved to: logs/storage_predictions.png")
            else:
                print("Failed to generate predictions.")
        else:
            print("Failed to train model.")
    else:
        print("No data available for training.")

if __name__ == "__main__":
    main()
Subtask 2.3: Running the Storage Prediction System

Let's execute our storage prediction system:

# Navigate to project directory
cd ~/storage_ai_lab

# Activate virtual environment
source storage_ai_env/bin/activate

# First, collect some sample data
python3 scripts/data_collector.py

# Wait for data collection to complete, then run predictions
python3 scripts/storage_predictor.py
Task 3: Implement AI-Based Monitoring for Storage Systems

Subtask 3.1: Creating Real-Time Storage Monitor

# File: scripts/storage_monitor.py
import psutil
import time
import json
import threading
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
import os

class AIStorageMonitor:
    def __init__(self, config_file="config/monitor_config.json"):
        self.config_file = config_file
        self.config = self.load_config()
        self.setup_logging()
        self.alert_history = []
        self.monitoring = False
        
    def load_config(self):
        """Load monitoring configuration"""
        default_config = {
            "thresholds": {
                "warning": 75,
                "critical": 90,
                "emergency": 95
            },
            "monitoring_interval": 30,
            "alert_cooldown": 300,
            "email_alerts": {
                "enabled": False,
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender_email": "",
                "sender_password": "",
                "recipient_email": ""
            },
            "auto_cleanup": {
                "enabled": True,
                "temp_dirs": ["/tmp", "/var/tmp"],
                "log_retention_days": 7
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults
                for key in default_config:
                    if key not in config:
                        config[key] = default_config[key]
                return config
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
        
        # Create config directory and save default config
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(default_config, f, indent=2)
        
        return default_config
    
    def setup_logging(self):
        """Setup logging configuration"""
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/storage_monitor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_storage_status(self):
        """Get current storage status"""
        disk_usage = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        
        status = {
            'timestamp': datetime.now().isoformat(),
            'total_gb': round(disk_usage.total / (1024**3), 2),
            'used_gb': round(disk_usage.used / (1024**3), 2),
            'free_gb': round(disk_usage.free / (1024**3), 2),
            'usage_percent': round((disk_usage.used / disk_usage.total) * 100, 2),
            'io_stats': {
                'read_count': disk_io.read_count if disk_io else 0,
                'write_count': disk_io.write_count if disk_io else 0,
                'read_bytes': disk_io.read_bytes if disk_io else 0,
                'write_bytes': disk_io.write_bytes if disk_io else 0
            }
        }
        
        return status
    
    def analyze_storage_trend(self, current_status):
        """Analyze storage usage trends using simple AI logic"""
        # This is a simplified AI analysis
        # In a real-world scenario, you'd use more sophisticated ML models
        
        usage_percent = current_status['usage_percent']
        analysis = {
            'current_usage': usage_percent,
            'trend': 'stable',
            'risk_level': 'low',
            'recommendations': []
        }
        
        # Determine risk level
        if usage_percent >= self.config['thresholds']['emergency']:
            analysis['risk_level'] = 'emergency'
            analysis['trend'] = 'critical'
        elif usage_percent >= self.config['thresholds']['critical']:
            analysis['risk_level'] = 'critical'
            analysis['trend'] = 'increasing'
        elif usage_percent >= self.config['thresholds']['warning']:
            analysis['risk_level'] = 'warning'
            analysis['trend'] = 'moderate'
        
        # Generate recommendations based on AI analysis
        if analysis['risk_level'] in ['critical', 'emergency']:
            analysis['recommendations'].extend([
                'Immediate cleanup required',
                'Stop non-essential services',
                'Archive or delete large files',
                'Consider emergency storage expansion'
            ])
        elif analysis['risk_level'] == 'warning':
            analysis['recommendations'].extend([
                'Schedule regular cleanup',
                'Monitor large file growth',
                'Plan storage capacity upgrade'
            ])
        
        return analysis
    
    def auto_cleanup(self):
        """Perform automatic cleanup based on AI recommendations"""
        if not self.config['auto_cleanup']['enabled']:
            return
        
        cleanup_actions = []
        
        # Clean temporary directories
        for temp_dir in self.config['auto_cleanup']['temp_dirs']:
            if os.path.exists(temp_dir):
                try:
                    # Count files before cleanup
                    files_before = len([f for f in os.listdir(temp_dir) 
                                      if os.path.isfile(os.path.join(temp_dir, f))])
                    
                    # Simple cleanup: remove files older than 1 day
                    import glob
                    import time
                    
                    temp_files = glob.glob(os.path.join(temp_dir, '*'))
                    removed_count = 0
                    
                    for file_path in temp_files:
                        try:
                            if os.path.isfile(file_path):
                                # Check if file is older than 1 day
                                if time.time() - os.path.getmtime(file_path) > 86400:
                                    os.remove(file_path)
                                    removed_count += 1
                        except Exception as e:
                            continue
                    
                    if removed_count > 0:
                        cleanup_actions.append(f"Removed {removed_count} temporary files from {temp_dir}")
                        
                except Exception as e:
                    self.logger.error(f"Error cleaning {temp_dir}: {e}")
        
        # Log cleanup actions
        if cleanup_actions:
            self.logger.info("Auto-cleanup completed:")
            for action in cleanup_actions:
                self.logger.info(f"  - {action}")
        
        return cleanup_actions
    
    def send_alert(self, status, analysis):
        """Send alert based on storage analysis"""
        alert_message = f"""
        STORAGE ALERT - {analysis['risk_level'].upper()}
        
        Current Usage: {status['usage_percent']}%
        Free Space: {status['free_gb']} GB
        Trend: {analysis['trend']}
        
        Recommendations:
        {chr(10).join(['• ' + rec for rec in analysis['recommendations']])}
        
        Timestamp: {status['timestamp']}
        """
        
        # Log alert
        self.logger.warning(alert_message)
        
        # Add to alert history
        self.alert_history.append({
            'timestamp': status['timestamp'],
            'level': analysis['risk_level'],
            'usage': status['usage_percent'],
            'message': alert_message
        })
        
        # Send email alert if configured
        if self.config['email_alerts']['enabled']:
            self.send_email_alert(alert_message, analysis['risk_level'])
    
    def send_email_alert(self, message, level):
        """Send email alert"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.config['email_alerts']['sender_email']
            msg['To'] = self.config['email_alerts']['recipient_email']
            msg['Subject'] = f"Storage Alert - {level.upper()}"
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(
                self.config['email_alerts']['smtp_server'],
                self.config['email_alerts']['smtp_port']
            )
            server.starttls()
            server.login(
                self.config['email_alerts']['sender_email'],
                self.config['email_alerts']['sender_password']
            )
            
            text = msg.as_string()
            server.sendmail(
                self.config['email_alerts']['sender_email'],
                self.config['email_alerts']['recipient_email'],
                text
            )
            server.quit()
            
            self.logger.info("Email alert sent successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
    
    def monitor_loop(self):
        """Main monitoring loop"""
        self.logger.info("Starting AI-driven storage monitoring...")
        
        while self.monitoring:
            try:
                # Get current storage status
                status = self.get_storage_status()
                
                # Perform AI analysis
                analysis = self.analyze_storage_trend(status)
                
                # Log current status
                self.logger.info(f"Storage: {status['usage_percent']}% used, "
                               f"{status['free_gb']} GB free, Risk: {analysis['risk_level']}")
                
                # Check if alert is needed
                if analysis['risk_level'] in ['warning', 'critical', 'emergency']:
                    # Check alert cooldown
                    current_time = datetime.now()
                    last_alert = None
                    
                    if self.alert_history:
                        last_alert_time = datetime.fromisoformat(self.alert_history[-1]['timestamp'])
                        time_diff = (current_time - last_alert_time).total_seconds()
                        
                        if time_diff < self.config['alert_cooldown']:
                            self.logger.debug("Alert cooldown active, skipping alert")
                        else:
                            self.send_alert(status, analysis)
                    else:
                        self.send_alert(status, analysis)
                
                # Perform auto-cleanup if needed
                if analysis['risk_level'] in ['critical', 'emergency']:
                    cleanup_actions = self.auto_cleanup()
                    if cleanup_actions:
                        self.logger.info("Auto-cleanup performed due to critical storage level")
                
                # Wait for next monitoring cycle
                time.sleep(self.config['monitoring_interval'])
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(10)  # Wait before retrying
    
    def start_monitoring(self):
        """Start monitoring in a separate thread"""
        if self.monitoring:
            self.logger.warning("Monitoring is already running")
            return
        
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self.monitor_loop)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        self.logger.info("AI Storage Monitor started successfully")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        if hasattr(self, 'monitor_thread'):
            self.monitor_thread.join(timeout=5)
        
        self.logger.info("AI Storage Monitor stopped")
    
    def get_status_report(self):
        """Generate comprehensive status report"""
        status = self.get_storage_status()
        analysis = self.analyze_storage_trend(status)
        
        report = {
            'current_status': status,
            'ai_analysis': analysis,
            'recent_alerts': self.alert_history[-5:] if self.alert_history else [],
            'monitoring_config': self.config
        }
        
        return report

def main():
    monitor = AIStorageMonitor()
    
    try:
        # Start monitoring
        monitor.start_monitoring()
        
        print("AI Storage Monitor is running...")
        print("Press Ctrl+C to stop monitoring")
        print("\nCurrent Status:")
        
        # Display initial status
        report = monitor.get_status_report()
        print(f"Storage Usage: {report['current_status']['usage_percent']}%")
        print(f"Free Space: {report['current_status']['free_gb']} GB")
        print(f"Risk Level: {report['ai_analysis']['risk_level']}")
        
        # Keep the main thread alive
        while True:
            time.sleep(60)  # Display status every minute
            report = monitor.get_status_report()
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] "
                  f"Usage: {report['current_status']['usage_percent']}% | "
                  f"Risk: {report['ai_analysis']['risk_level']}")
            
    except KeyboardInterrupt:
        print("\nStopping AI Storage Monitor...")
        monitor.stop_monitoring()
        print("Monitor stopped successfully")

if __name__ == "__main__":
    main()
Subtask 3.2: Creating Configuration and Testing

Let's create a configuration file and test our monitoring system:

# Create configuration directory
mkdir -p ~/storage_ai_lab/config

# Create a sample configuration file
cat > ~/storage_ai_lab/config/monitor_config.json << 'EOF'
{
  "thresholds": {
    "warning": 70,
    "critical": 85,
    "emergency": 95
  },
  "monitoring_interval": 15,
  "alert_cooldown": 180,
  "email_alerts": {
    "enabled": false,
    "smtp_server": "smtp.gmail.com",
    "smtp_port": 587,
    "sender_email": "",
    "sender_password": "",
    "recipient_email": ""
  },
  "auto_cleanup": {
    "enabled": true,
    "temp_dirs": ["/tmp", "/var/tmp"],
    "log_retention_days": 7
  }
}
EOF
Subtask 3.3: Running the AI Storage Monitor

# Navigate to project directory
cd ~/storage_ai_lab

# Activate virtual environment
source storage_ai_env/bin/activate

# Run the AI storage monitor
python3 scripts/storage_monitor.py
Subtask 3.4: Creating a Comprehensive Dashboard Script

Let's create a dashboard to visualize all our AI-driven storage insights:

# File: scripts/storage_dashboard.py
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
import os
from datetime import datetime, timedelta
import numpy as np

class StorageDashboard:
    def __init__(self):
        self.setup_style()
    
    def setup_style(self):
        """Setup plotting style"""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
    
    def load_monitoring_data(self):
        """Load data from various sources"""
        data = {}
        
        # Load storage metrics
        if os.path.exists("data/storage_metrics.csv"):
            data['metrics'] = pd.read_csv("data/storage_metrics.csv")
            data['metrics']['timestamp'] = pd.to_datetime(data['metrics']['timestamp'])
        
        # Load alert history from logs
        alert_data = []
        if os.path.exists("logs/storage_monitor.log"):
            with open("logs/storage_monitor.log", 'r') as f:
                for line in f:
                    if "STORAGE ALERT" in line:
                        # Parse alert information (simplified)
                        alert_data.append({
                            'timestamp': datetime.now(),
                            'level': 'warning',
                            'message': line.strip()
                        })
        
        data['alerts'] = alert_data
        return data
    
    def create_usage_trend_chart(self, metrics_df):
        """Create storage usage trend chart"""
        if metrics_df is None or len(metrics_df) == 0:
            return None
        
        fig,
