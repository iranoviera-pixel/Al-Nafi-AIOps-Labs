AI-Driven Network Configuration and Monitoring

Objectives

By the end of this lab, students will be able to:

Understand the fundamentals of AI-driven network management
Research and identify open-source AI tools for network optimization
Implement machine learning algorithms to predict network traffic patterns
Create automated network configuration adjustments based on AI predictions
Deploy AI-based monitoring systems for real-time network performance analysis
Analyze network data using machine learning techniques
Build a complete AI-driven network monitoring solution
Prerequisites

Before starting this lab, students should have:

Basic understanding of networking concepts (IP addresses, ports, protocols)
Fundamental knowledge of Python programming
Familiarity with Linux command line operations
Basic understanding of machine learning concepts
Knowledge of network monitoring principles
Required Software Knowledge:

Python 3.x
Basic Linux commands
Text editors (nano, vim, or similar)
Lab Environment Setup

Al Nafi Cloud Machine Access: This lab uses Al Nafi's pre-configured Linux-based cloud machines. Simply click Start Lab to access your ready-to-use environment. No need to build your own virtual machine or install additional software - everything is pre-installed and configured for you.

What's Pre-installed:

Python 3.x with pip
Essential networking tools
Required Python libraries
Sample network data files
Task 1: Research AI Tools for Network Optimization and Monitoring

Subtask 1.1: Understanding AI in Network Management

Step 1: Access your cloud machine and create a working directory

mkdir ~/ai-network-lab
cd ~/ai-network-lab
Step 2: Create a research documentation file

nano ai_network_tools_research.md
Step 3: Add the following research content to understand key AI tools:

# AI Tools for Network Management Research

## Open Source AI Tools for Network Optimization:

### 1. Scikit-learn
- Purpose: Machine learning library for traffic prediction
- Use Case: Anomaly detection, traffic pattern analysis
- Installation: pip install scikit-learn

### 2. TensorFlow/Keras
- Purpose: Deep learning for complex network behavior prediction
- Use Case: Advanced traffic forecasting, network optimization
- Installation: pip install tensorflow

### 3. NetworkX
- Purpose: Network topology analysis and optimization
- Use Case: Network graph analysis, path optimization
- Installation: pip install networkx

### 4. Pandas + NumPy
- Purpose: Data manipulation and numerical computing
- Use Case: Network data processing and analysis
- Installation: pip install pandas numpy

### 5. Matplotlib/Seaborn
- Purpose: Data visualization
- Use Case: Network performance visualization
- Installation: pip install matplotlib seaborn

## AI Applications in Network Management:

1. **Traffic Prediction**: Using historical data to predict future network load
2. **Anomaly Detection**: Identifying unusual network behavior
3. **Auto-scaling**: Automatically adjusting network resources
4. **Quality of Service (QoS) Optimization**: Prioritizing traffic intelligently
5. **Fault Prediction**: Predicting network failures before they occur
Save and exit the file (Ctrl+X, then Y, then Enter).

Subtask 1.2: Install Required Python Libraries

Step 1: Update the system and install Python dependencies

sudo apt update
pip3 install --upgrade pip
Step 2: Install the AI and networking libraries

pip3 install scikit-learn pandas numpy matplotlib seaborn networkx psutil
Step 3: Verify installations

python3 -c "import sklearn, pandas, numpy, matplotlib, networkx, psutil; print('All libraries installed successfully')"
Task 2: Write Python Script for Traffic Prediction and Configuration

Subtask 2.1: Create Network Traffic Data Generator

Step 1: Create a script to generate sample network traffic data

nano traffic_data_generator.py
Step 2: Add the following code:

#!/usr/bin/env python3
"""
Network Traffic Data Generator
Generates realistic network traffic data for AI training
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class NetworkTrafficGenerator:
    def __init__(self):
        self.base_traffic = 100  # Base traffic in Mbps
        
    def generate_hourly_pattern(self, hours=24):
        """Generate traffic pattern based on typical daily usage"""
        traffic_pattern = []
        
        for hour in range(hours):
            # Simulate daily traffic patterns
            if 0 <= hour < 6:  # Night time - low traffic
                base_multiplier = 0.3
            elif 6 <= hour < 9:  # Morning peak
                base_multiplier = 0.8
            elif 9 <= hour < 17:  # Business hours
                base_multiplier = 1.0
            elif 17 <= hour < 21:  # Evening peak
                base_multiplier = 1.2
            else:  # Late evening
                base_multiplier = 0.6
                
            # Add random variation
            noise = random.uniform(0.8, 1.2)
            traffic = self.base_traffic * base_multiplier * noise
            
            traffic_pattern.append({
                'hour': hour,
                'traffic_mbps': round(traffic, 2),
                'cpu_usage': round(min(traffic * 0.5, 100), 2),
                'memory_usage': round(min(traffic * 0.3 + 20, 90), 2),
                'active_connections': int(traffic * 10),
                'packet_loss': round(max(0, (traffic - 80) * 0.01), 3)
            })
            
        return traffic_pattern
    
    def generate_weekly_data(self):
        """Generate a week's worth of traffic data"""
        weekly_data = []
        
        for day in range(7):
            daily_data = self.generate_hourly_pattern()
            for hour_data in daily_data:
                hour_data['day'] = day
                hour_data['timestamp'] = datetime.now() - timedelta(days=6-day, hours=23-hour_data['hour'])
                weekly_data.append(hour_data)
                
        return pd.DataFrame(weekly_data)

if __name__ == "__main__":
    generator = NetworkTrafficGenerator()
    
    # Generate sample data
    print("Generating network traffic data...")
    traffic_data = generator.generate_weekly_data()
    
    # Save to CSV
    traffic_data.to_csv('network_traffic_data.csv', index=False)
    print(f"Generated {len(traffic_data)} data points")
    print("Data saved to 'network_traffic_data.csv'")
    
    # Display sample data
    print("\nSample data:")
    print(traffic_data.head(10))
Step 3: Run the data generator

python3 traffic_data_generator.py
Subtask 2.2: Create AI Traffic Prediction Model

Step 1: Create the main AI prediction script

nano ai_traffic_predictor.py
Step 2: Add the comprehensive AI prediction code:

#!/usr/bin/env python3
"""
AI-Driven Network Traffic Predictor
Uses machine learning to predict network traffic and adjust configurations
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import joblib
import warnings
warnings.filterwarnings('ignore')

class AINetworkPredictor:
    def __init__(self):
        self.model = None
        self.feature_columns = ['hour', 'day', 'cpu_usage', 'memory_usage', 'active_connections']
        self.target_column = 'traffic_mbps'
        
    def load_data(self, filename='network_traffic_data.csv'):
        """Load network traffic data"""
        try:
            data = pd.read_csv(filename)
            print(f"Loaded {len(data)} records from {filename}")
            return data
        except FileNotFoundError:
            print(f"Error: {filename} not found. Please run traffic_data_generator.py first.")
            return None
    
    def prepare_features(self, data):
        """Prepare features for machine learning"""
        # Create additional time-based features
        data['hour_sin'] = np.sin(2 * np.pi * data['hour'] / 24)
        data['hour_cos'] = np.cos(2 * np.pi * data['hour'] / 24)
        data['day_sin'] = np.sin(2 * np.pi * data['day'] / 7)
        data['day_cos'] = np.cos(2 * np.pi * data['day'] / 7)
        
        # Add lag features (previous hour's traffic)
        data['prev_traffic'] = data['traffic_mbps'].shift(1)
        data['prev_cpu'] = data['cpu_usage'].shift(1)
        
        # Fill NaN values
        data = data.fillna(method='bfill')
        
        # Update feature columns
        self.feature_columns = ['hour', 'day', 'cpu_usage', 'memory_usage', 
                               'active_connections', 'hour_sin', 'hour_cos', 
                               'day_sin', 'day_cos', 'prev_traffic', 'prev_cpu']
        
        return data
    
    def train_model(self, data):
        """Train the AI model"""
        print("Training AI model...")
        
        # Prepare features
        X = data[self.feature_columns]
        y = data[self.target_column]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train Random Forest model
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        print(f"Model Performance:")
        print(f"Mean Squared Error: {mse:.2f}")
        print(f"R² Score: {r2:.3f}")
        
        # Save model
        joblib.dump(self.model, 'network_traffic_model.pkl')
        print("Model saved as 'network_traffic_model.pkl'")
        
        return X_test, y_test, y_pred
    
    def predict_traffic(self, hour, day, cpu_usage, memory_usage, active_connections, 
                       prev_traffic=100, prev_cpu=50):
        """Predict traffic for given parameters"""
        if self.model is None:
            try:
                self.model = joblib.load('network_traffic_model.pkl')
            except FileNotFoundError:
                print("Error: No trained model found. Please train the model first.")
                return None
        
        # Prepare features
        hour_sin = np.sin(2 * np.pi * hour / 24)
        hour_cos = np.cos(2 * np.pi * hour / 24)
        day_sin = np.sin(2 * np.pi * day / 7)
        day_cos = np.cos(2 * np.pi * day / 7)
        
        features = np.array([[hour, day, cpu_usage, memory_usage, active_connections,
                            hour_sin, hour_cos, day_sin, day_cos, prev_traffic, prev_cpu]])
        
        prediction = self.model.predict(features)[0]
        return round(prediction, 2)
    
    def generate_network_config(self, predicted_traffic):
        """Generate network configuration based on predicted traffic"""
        config = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'predicted_traffic_mbps': predicted_traffic,
            'recommendations': []
        }
        
        # Traffic-based recommendations
        if predicted_traffic < 50:
            config['bandwidth_allocation'] = 'Low'
            config['qos_priority'] = 'Standard'
            config['recommendations'].append('Reduce active network interfaces')
            config['recommendations'].append('Enable power saving mode')
            
        elif predicted_traffic < 100:
            config['bandwidth_allocation'] = 'Medium'
            config['qos_priority'] = 'Standard'
            config['recommendations'].append('Standard configuration')
            
        elif predicted_traffic < 150:
            config['bandwidth_allocation'] = 'High'
            config['qos_priority'] = 'High'
            config['recommendations'].append('Increase buffer sizes')
            config['recommendations'].append('Enable traffic shaping')
            
        else:
            config['bandwidth_allocation'] = 'Maximum'
            config['qos_priority'] = 'Critical'
            config['recommendations'].append('Scale up network resources')
            config['recommendations'].append('Enable load balancing')
            config['recommendations'].append('Monitor for potential bottlenecks')
        
        return config
    
    def visualize_predictions(self, X_test, y_test, y_pred):
        """Create visualizations of model performance"""
        plt.figure(figsize=(15, 10))
        
        # Actual vs Predicted
        plt.subplot(2, 2, 1)
        plt.scatter(y_test, y_pred, alpha=0.6)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        plt.xlabel('Actual Traffic (Mbps)')
        plt.ylabel('Predicted Traffic (Mbps)')
        plt.title('Actual vs Predicted Traffic')
        
        # Residuals
        plt.subplot(2, 2, 2)
        residuals = y_test - y_pred
        plt.scatter(y_pred, residuals, alpha=0.6)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('Predicted Traffic (Mbps)')
        plt.ylabel('Residuals')
        plt.title('Residual Plot')
        
        # Feature Importance
        plt.subplot(2, 2, 3)
        importance = self.model.feature_importances_
        features = self.feature_columns
        indices = np.argsort(importance)[::-1]
        
        plt.bar(range(len(importance)), importance[indices])
        plt.xticks(range(len(importance)), [features[i] for i in indices], rotation=45)
        plt.title('Feature Importance')
        
        # Time series prediction sample
        plt.subplot(2, 2, 4)
        sample_size = min(50, len(y_test))
        plt.plot(range(sample_size), y_test.iloc[:sample_size], label='Actual', marker='o')
        plt.plot(range(sample_size), y_pred[:sample_size], label='Predicted', marker='s')
        plt.xlabel('Time Points')
        plt.ylabel('Traffic (Mbps)')
        plt.title('Sample Predictions Over Time')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig('ai_prediction_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
        print("Visualization saved as 'ai_prediction_analysis.png'")

def main():
    predictor = AINetworkPredictor()
    
    # Load and prepare data
    data = predictor.load_data()
    if data is None:
        return
    
    data = predictor.prepare_features(data)
    
    # Train model
    X_test, y_test, y_pred = predictor.train_model(data)
    
    # Create visualizations
    predictor.visualize_predictions(X_test, y_test, y_pred)
    
    # Example predictions
    print("\n" + "="*50)
    print("EXAMPLE TRAFFIC PREDICTIONS AND CONFIGURATIONS")
    print("="*50)
    
    scenarios = [
        {'hour': 3, 'day': 1, 'cpu': 30, 'memory': 40, 'connections': 500, 'desc': 'Night time'},
        {'hour': 9, 'day': 2, 'cpu': 70, 'memory': 60, 'connections': 1200, 'desc': 'Morning peak'},
        {'hour': 14, 'day': 3, 'cpu': 85, 'memory': 75, 'connections': 1500, 'desc': 'Business hours'},
        {'hour': 19, 'day': 4, 'cpu': 90, 'memory': 80, 'connections': 1800, 'desc': 'Evening peak'}
    ]
    
    for scenario in scenarios:
        predicted_traffic = predictor.predict_traffic(
            scenario['hour'], scenario['day'], scenario['cpu'], 
            scenario['memory'], scenario['connections']
        )
        
        config = predictor.generate_network_config(predicted_traffic)
        
        print(f"\nScenario: {scenario['desc']}")
        print(f"Time: {scenario['hour']}:00, Day: {scenario['day']}")
        print(f"Current: CPU {scenario['cpu']}%, Memory {scenario['memory']}%, Connections: {scenario['connections']}")
        print(f"Predicted Traffic: {predicted_traffic} Mbps")
        print(f"Bandwidth Allocation: {config['bandwidth_allocation']}")
        print(f"QoS Priority: {config['qos_priority']}")
        print("Recommendations:")
        for rec in config['recommendations']:
            print(f"  - {rec}")

if __name__ == "__main__":
    main()
Step 3: Run the AI traffic predictor

python3 ai_traffic_predictor.py
Subtask 2.3: Create Network Configuration Automation Script

Step 1: Create an automated configuration script

nano network_config_automation.py
Step 2: Add the automation code:

#!/usr/bin/env python3
"""
Network Configuration Automation
Automatically adjusts network settings based on AI predictions
"""

import subprocess
import json
import time
from datetime import datetime
import psutil
import joblib
import numpy as np

class NetworkConfigAutomation:
    def __init__(self):
        self.config_file = 'current_network_config.json'
        self.log_file = 'network_automation.log'
        
    def get_current_system_stats(self):
        """Get current system statistics"""
        current_time = datetime.now()
        
        stats = {
            'hour': current_time.hour,
            'day': current_time.weekday(),
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().percent,
            'active_connections': len(psutil.net_connections()),
            'network_io': psutil.net_io_counters(),
            'timestamp': current_time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return stats
    
    def predict_traffic_load(self, stats):
        """Predict traffic using the trained model"""
        try:
            model = joblib.load('network_traffic_model.pkl')
            
            # Prepare features (same as training)
            hour_sin = np.sin(2 * np.pi * stats['hour'] / 24)
            hour_cos = np.cos(2 * np.pi * stats['hour'] / 24)
            day_sin = np.sin(2 * np.pi * stats['day'] / 7)
            day_cos = np.cos(2 * np.pi * stats['day'] / 7)
            
            # Use current stats as previous values for simplicity
            features = np.array([[
                stats['hour'], stats['day'], stats['cpu_usage'], 
                stats['memory_usage'], stats['active_connections'],
                hour_sin, hour_cos, day_sin, day_cos,
                100, stats['cpu_usage']  # prev_traffic, prev_cpu
            ]])
            
            prediction = model.predict(features)[0]
            return round(prediction, 2)
            
        except FileNotFoundError:
            print("Warning: AI model not found. Using fallback prediction.")
            # Fallback: simple heuristic based on current load
            base_traffic = 50
            load_factor = (stats['cpu_usage'] + stats['memory_usage']) / 200
            return round(base_traffic * (1 + load_factor), 2)
    
    def generate_network_commands(self, predicted_traffic, current_stats):
        """Generate network configuration commands"""
        commands = []
        config_changes = []
        
        # Traffic Control (tc) commands for bandwidth management
        interface = self.get_primary_interface()
        
        if predicted_traffic < 50:
            # Low traffic - conservative settings
            bandwidth = "50mbit"
            buffer_size = "1000"
            config_changes.append("Low traffic mode: Conservative bandwidth allocation")
            
        elif predicted_traffic < 100:
            # Medium traffic - standard settings
            bandwidth = "100mbit"
            buffer_size = "2000"
            config_changes.append("Medium traffic mode: Standard bandwidth allocation")
            
        elif predicted_traffic < 150:
            # High traffic - optimized settings
            bandwidth = "200mbit"
            buffer_size = "4000"
            config_changes.append("High traffic mode: Optimized bandwidth allocation")
            
        else:
            # Very high traffic - maximum settings
            bandwidth = "500mbit"
            buffer_size = "8000"
            config_changes.append("Peak traffic mode: Maximum bandwidth allocation")
        
        # Generate tc commands (these would need root privileges in real deployment)
        commands.extend([
            f"# Traffic control commands for {interface}",
            f"sudo tc qdisc del dev {interface} root 2>/dev/null || true",
            f"sudo tc qdisc add dev {interface} root handle 1: htb default 30",
            f"sudo tc class add dev {interface} parent 1: classid 1:1 htb rate {bandwidth}",
            f"sudo tc class add dev {interface} parent 1:1 classid 1:10 htb rate {bandwidth} ceil {bandwidth}",
        ])
        
        # System optimization commands
        if predicted_traffic > 100:
            commands.extend([
                "# System optimization for high traffic",
                "echo 'net.core.rmem_max = 16777216' | sudo tee -a /etc/sysctl.conf",
                "echo 'net.core.wmem_max = 16777216' | sudo tee -a /etc/sysctl.conf",
                "sudo sysctl -p"
            ])
            config_changes.append("Applied high-traffic system optimizations")
        
        return commands, config_changes
    
    def get_primary_interface(self):
        """Get the primary network interface"""
        try:
            # Get default route interface
            result = subprocess.run(['ip', 'route', 'show', 'default'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                # Parse interface from default route
                parts = result.stdout.split()
                if 'dev' in parts:
                    idx = parts.index('dev')
                    if idx + 1 < len(parts):
                        return parts[idx + 1]
            
            # Fallback to first non-loopback interface
            interfaces = psutil.net_if_addrs()
            for interface in interfaces:
                if interface != 'lo' and not interface.startswith('docker'):
                    return interface
                    
        except Exception as e:
            print(f"Error getting primary interface: {e}")
        
        return 'eth0'  # Default fallback
    
    def apply_configuration(self, commands, config_changes, dry_run=True):
        """Apply network configuration (dry run by default for safety)"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        config_log = {
            'timestamp': timestamp,
            'commands': commands,
            'changes': config_changes,
            'dry_run': dry_run
        }
        
        if dry_run:
            print(f"\n[{timestamp}] DRY RUN - Configuration changes that would be applied:")
            print("-" * 60)
            for change in config_changes:
                print(f"✓ {change}")
            
            print(f"\nCommands that would be executed:")
            for cmd in commands:
                if not cmd.startswith('#'):
                    print(f"  {cmd}")
                else:
                    print(f"\n{cmd}")
        else:
            print(f"\n[{timestamp}] Applying network configuration changes...")
            for cmd in commands:
                if not cmd.startswith('#') and cmd.strip():
                    try:
                        result = subprocess.run(cmd.split(), capture_output=True, text=True)
                        if result.returncode != 0:
                            print(f"Warning: Command failed: {cmd}")
                            print(f"Error: {result.stderr}")
                    except Exception as e:
                        print(f"Error executing command '{cmd}': {e}")
        
        # Log the configuration
        self.log_configuration(config_log)
        
        return config_log
    
    def log_configuration(self, config_log):
        """Log configuration changes"""
        try:
            with open(self.log_file, 'a') as f:
                f.write(json.dumps(config_log, indent=2) + '\n')
        except Exception as e:
            print(f"Error logging configuration: {e}")
    
    def monitor_and_adjust(self, duration_minutes=10, check_interval=60):
        """Continuously monitor and adjust network configuration"""
        print(f"Starting AI-driven network monitoring for {duration_minutes} minutes...")
        print(f"Checking every {check_interval} seconds")
        print("Note: Running in DRY RUN mode for safety")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        
        while time.time() < end_time:
            try:
                # Get current system stats
                stats = self.get_current_system_stats()
                
                # Predict traffic
                predicted_traffic = self.predict_traffic_load(stats)
                
                # Generate configuration
                commands, changes = self.generate_network_commands(predicted_traffic, stats)
                
                # Apply configuration (dry run)
                config_log = self.apply_configuration(commands, changes, dry_run=True)
                
                print(f"\nCurrent Stats:")
                print(f"  CPU: {stats['cpu_usage']:.1f}%")
                print(f"  Memory: {stats['memory_usage']:.1f}%")
                print(f"  Connections: {stats['active_connections']}")
                print(f"  Predicted Traffic: {predicted_traffic} Mbps")
                
                # Wait for next check
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user.")
                break
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(check_interval)
        
        print("Monitoring completed.")

def main():
    automation = NetworkConfigAutomation()
    
    print("AI-Driven Network Configuration Automation")
    print("=" * 50)
    
    # Get current system stats
    stats = automation.get_current_system_stats()
    print(f"Current System Stats:")
    print(f"  Time: {stats['timestamp']}")
    print(f"  CPU Usage: {stats['cpu_usage']:.1f}%")
    print(f"  Memory Usage: {stats['memory_usage']:.1f}%")
    print(f"  Active Connections: {stats['active_connections']}")
    
    # Predict traffic
    predicted_traffic = automation.predict_traffic_load(stats)
    print(f"  Predicted Traffic: {predicted_traffic} Mbps")
    
    # Generate and apply configuration
    commands, changes = automation.generate_network_commands(predicted_traffic, stats)
    automation.apply_configuration(commands, changes, dry_run=True)
    
    # Ask user if they want to start continuous monitoring
    print(f"\nWould you like to start continuous monitoring? (y/n): ", end="")
    response = input().lower().strip()
    
    if response == 'y':
        automation.monitor_and_adjust(duration_minutes=5, check_interval=30)

if __name__ == "__main__":
    main()
Step 3: Run the network automation script

python3 network_config_automation.py
Task 3: Implement AI-Based Monitoring for Network Performance

Subtask 3.1: Create Real-Time Network Monitor

Step 1: Create a comprehensive network monitoring script

nano ai_network_monitor.py
Step 2: Add the monitoring code:

#!/usr/bin/env python3
"""
AI-Based Network Performance Monitor
Real-time monitoring with anomaly detection and alerting
"""

import psutil
import time
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import threading
import queue
import warnings
warnings.filterwarnings('ignore')

class AINetworkMonitor:
    def __init__(self):
        self.monitoring = False
        self.data_queue = queue.Queue()
        self.historical_data = []
        self.anomaly_detector = None
        self.scaler = StandardScaler()
        self.alert_threshold = 0.8
        self.monitoring_interval = 5  # seconds
        
    def collect_network_metrics(self):
        """Collect comprehensive network metrics"""
        try:
            # Network I/O statistics
            net_io = psutil.net_io_counters()
            
            # Network connections
            connections = psutil.net_connections()
            active_connections = len([c for c in connections if c.status == 'ESTABLISHED'])
            
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            # Network interface statistics
            net_if_stats = psutil.net_if_stats()
            
            # Calculate network utilization
            total_bytes = net_io.bytes_sent + net_io.bytes_recv
            
            metrics = {
                'timestamp': datetime.now(),
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
                'errin': net_io.errin,
                'errout': net_io.errout,
                'dropin': net_io.dropin,
                'dropout': net_io.dropout,
                'active_connections': active_connections,
                'total_connections': len(connections),
                'cpu_percent': cpu_percent,
                'memory_percent': memory.percent,
                'memory_available': memory.available,
                'total_bytes': total_bytes,
                'network_utilization': self.calculate_network_utilization(net_io)
            }
            
            return metrics
            
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            return None
    
    def calculate_network_utilization(self, net_io):
        """Calculate network utilization percentage"""
        # This is a simplified calculation
        # In real scenarios, you'd need interface speed information
        max_bandwidth_bps = 1000000000  # Assume 1 Gbps interface
        current_bps = (net_io.bytes_sent + net_io.bytes_recv) / self.monitoring_interval
