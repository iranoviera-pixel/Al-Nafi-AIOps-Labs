Lab 80: AI-Powered Container Management and Optimization

Lab Objectives

By the end of this lab, students will be able to:

Understand the fundamentals of AI-driven container resource optimization
Research and identify open-source AI tools suitable for container management
Develop a Python-based machine learning script for predicting container resource usage
Integrate AI optimization capabilities with Podman container runtime
Implement automated resource allocation based on historical data patterns
Monitor and evaluate the effectiveness of AI-powered container optimization
Prerequisites

Before starting this lab, students should have:

Basic understanding of containerization concepts (Docker/Podman)
Fundamental knowledge of Python programming
Basic familiarity with machine learning concepts
Understanding of Linux command-line operations
Knowledge of system resource monitoring (CPU, memory, disk)
Lab Environment Setup

Ready-to-Use Cloud Machines: Al Nafi provides pre-configured Linux-based cloud machines for this lab. Simply click Start Lab to access your environment - no need to build your own VM or install additional software.

Your cloud machine comes pre-installed with:

Python 3.8+
Podman container runtime
Required Python libraries for machine learning
Sample container applications for testing
Task 1: Research AI Tools for Container Resource Optimization

Subtask 1.1: Understanding AI-Powered Container Management

Container resource optimization using AI involves analyzing historical usage patterns, predicting future resource needs, and automatically adjusting resource allocations to improve efficiency and performance.

Key Benefits:

Predictive Scaling: Anticipate resource needs before bottlenecks occur
Cost Optimization: Reduce over-provisioning and waste
Performance Enhancement: Maintain optimal application performance
Automated Management: Reduce manual intervention requirements
Subtask 1.2: Exploring Open-Source AI Tools

Let's research and document available open-source tools for container optimization:

# Create a research directory
mkdir -p ~/ai-container-lab/research
cd ~/ai-container-lab/research

# Create a research documentation file
cat > ai_tools_research.md << 'EOF'
# AI Tools for Container Resource Optimization

## 1. Scikit-learn
- **Purpose**: Machine learning library for predictive modeling
- **Use Case**: Predicting resource usage patterns
- **Advantages**: Easy to use, well-documented, extensive algorithms

## 2. TensorFlow/Keras
- **Purpose**: Deep learning framework
- **Use Case**: Complex pattern recognition in resource usage
- **Advantages**: Powerful neural networks, time series analysis

## 3. Prometheus + Grafana
- **Purpose**: Monitoring and alerting
- **Use Case**: Data collection and visualization
- **Advantages**: Industry standard, excellent integration

## 4. Kubernetes Vertical Pod Autoscaler (VPA)
- **Purpose**: Automatic resource recommendation
- **Use Case**: Right-sizing container resources
- **Advantages**: Built-in Kubernetes integration

## 5. Custom Python Solutions
- **Purpose**: Tailored optimization algorithms
- **Use Case**: Specific business requirements
- **Advantages**: Full control, customizable logic
EOF

echo "Research documentation created successfully!"
Subtask 1.3: Setting Up the Development Environment

# Create project structure
mkdir -p ~/ai-container-lab/{scripts,data,models,logs}
cd ~/ai-container-lab

# Install required Python packages
pip3 install --user scikit-learn pandas numpy matplotlib seaborn psutil

# Verify installations
python3 -c "import sklearn, pandas, numpy, matplotlib; print('All packages installed successfully!')"
Task 2: Develop Machine Learning Script for Resource Prediction

Subtask 2.1: Create Data Collection Script

First, let's create a script to collect historical container resource usage data:

# Create data collection script
cat > ~/ai-container-lab/scripts/collect_metrics.py << 'EOF'
#!/usr/bin/env python3
"""
Container Resource Metrics Collection Script
Collects CPU, memory, and network usage data from running containers
"""

import json
import time
import subprocess
import psutil
import pandas as pd
from datetime import datetime
import os

class ContainerMetricsCollector:
    def __init__(self, output_file="container_metrics.csv"):
        self.output_file = output_file
        self.metrics_data = []
    
    def get_podman_containers(self):
        """Get list of running Podman containers"""
        try:
            result = subprocess.run(['podman', 'ps', '--format', 'json'], 
                                  capture_output=True, text=True, check=True)
            return json.loads(result.stdout)
        except subprocess.CalledProcessError:
            print("Error: Unable to get container list. Make sure Podman is running.")
            return []
    
    def get_container_stats(self, container_id):
        """Get resource statistics for a specific container"""
        try:
            result = subprocess.run(['podman', 'stats', '--no-stream', '--format', 'json', container_id],
                                  capture_output=True, text=True, check=True)
            stats = json.loads(result.stdout)[0]
            return {
                'container_id': container_id,
                'cpu_percent': float(stats.get('CPU', '0%').rstrip('%')),
                'memory_usage': self.parse_memory(stats.get('MemUsage', '0B / 0B')),
                'memory_percent': float(stats.get('MemPerc', '0%').rstrip('%')),
                'network_io': stats.get('NetIO', '0B / 0B'),
                'block_io': stats.get('BlockIO', '0B / 0B'),
                'timestamp': datetime.now().isoformat()
            }
        except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
            return None
    
    def parse_memory(self, memory_str):
        """Parse memory usage string (e.g., '100MB / 2GB')"""
        try:
            used = memory_str.split(' / ')[0]
            # Convert to MB for consistency
            if 'GB' in used:
                return float(used.replace('GB', '')) * 1024
            elif 'MB' in used:
                return float(used.replace('MB', ''))
            elif 'KB' in used:
                return float(used.replace('KB', '')) / 1024
            else:
                return float(used.replace('B', '')) / (1024 * 1024)
        except:
            return 0.0
    
    def collect_metrics(self, duration_minutes=5, interval_seconds=30):
        """Collect metrics for specified duration"""
        print(f"Starting metrics collection for {duration_minutes} minutes...")
        end_time = time.time() + (duration_minutes * 60)
        
        while time.time() < end_time:
            containers = self.get_podman_containers()
            
            for container in containers:
                container_id = container['Id'][:12]  # Short ID
                container_name = container['Names'][0]
                
                stats = self.get_container_stats(container_id)
                if stats:
                    stats['container_name'] = container_name
                    stats['system_cpu_percent'] = psutil.cpu_percent()
                    stats['system_memory_percent'] = psutil.virtual_memory().percent
                    self.metrics_data.append(stats)
                    print(f"Collected metrics for {container_name}: CPU {stats['cpu_percent']}%, Memory {stats['memory_percent']}%")
            
            time.sleep(interval_seconds)
        
        self.save_metrics()
    
    def save_metrics(self):
        """Save collected metrics to CSV file"""
        if self.metrics_data:
            df = pd.DataFrame(self.metrics_data)
            output_path = os.path.join(os.path.expanduser('~/ai-container-lab/data'), self.output_file)
            df.to_csv(output_path, index=False)
            print(f"Metrics saved to {output_path}")
            print(f"Total records collected: {len(self.metrics_data)}")
        else:
            print("No metrics data collected")

if __name__ == "__main__":
    collector = ContainerMetricsCollector()
    collector.collect_metrics(duration_minutes=2, interval_seconds=10)  # Short duration for demo
EOF

chmod +x ~/ai-container-lab/scripts/collect_metrics.py
Subtask 2.2: Create Sample Containers for Testing

# Start some sample containers to generate metrics
echo "Starting sample containers for testing..."

# Start a CPU-intensive container
podman run -d --name cpu-test alpine sh -c 'while true; do echo "CPU test" > /dev/null; done'

# Start a memory-intensive container
podman run -d --name memory-test alpine sh -c 'while true; do dd if=/dev/zero of=/tmp/test bs=1M count=100 2>/dev/null; sleep 5; rm -f /tmp/test; done'

# Start a simple web server
podman run -d --name web-test -p 8080:80 nginx:alpine

echo "Sample containers started. Checking status..."
podman ps
Subtask 2.3: Collect Sample Data

# Run the metrics collection script
cd ~/ai-container-lab
python3 scripts/collect_metrics.py

# Check if data was collected
ls -la data/
head data/container_metrics.csv
Subtask 2.4: Create Machine Learning Prediction Script

# Create the main ML prediction script
cat > ~/ai-container-lab/scripts/ai_optimizer.py << 'EOF'
#!/usr/bin/env python3
"""
AI-Powered Container Resource Optimizer
Uses machine learning to predict and optimize container resource allocation
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
import os
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class ContainerResourceOptimizer:
    def __init__(self, data_file="container_metrics.csv"):
        self.data_file = os.path.join(os.path.expanduser('~/ai-container-lab/data'), data_file)
        self.model_cpu = None
        self.model_memory = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        
    def load_and_prepare_data(self):
        """Load and prepare data for machine learning"""
        print("Loading and preparing data...")
        
        # Load data
        df = pd.read_csv(self.data_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Create time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['minute'] = df['timestamp'].dt.minute
        
        # Create lag features (previous values)
        df = df.sort_values(['container_name', 'timestamp'])
        df['cpu_lag1'] = df.groupby('container_name')['cpu_percent'].shift(1)
        df['memory_lag1'] = df.groupby('container_name')['memory_percent'].shift(1)
        df['cpu_lag2'] = df.groupby('container_name')['cpu_percent'].shift(2)
        df['memory_lag2'] = df.groupby('container_name')['memory_percent'].shift(2)
        
        # Create rolling averages
        df['cpu_rolling_avg'] = df.groupby('container_name')['cpu_percent'].rolling(window=3).mean().reset_index(0, drop=True)
        df['memory_rolling_avg'] = df.groupby('container_name')['memory_percent'].rolling(window=3).mean().reset_index(0, drop=True)
        
        # Encode container names
        df['container_encoded'] = pd.Categorical(df['container_name']).codes
        
        # Remove rows with NaN values (due to lag features)
        df = df.dropna()
        
        self.feature_columns = ['hour', 'day_of_week', 'minute', 'container_encoded',
                               'cpu_lag1', 'memory_lag1', 'cpu_lag2', 'memory_lag2',
                               'cpu_rolling_avg', 'memory_rolling_avg', 'system_cpu_percent', 'system_memory_percent']
        
        return df
    
    def train_models(self):
        """Train machine learning models for CPU and memory prediction"""
        print("Training machine learning models...")
        
        df = self.load_and_prepare_data()
        
        if len(df) < 10:
            print("Warning: Limited data available. Consider collecting more metrics for better predictions.")
            # Generate synthetic data for demonstration
            df = self.generate_synthetic_data()
        
        # Prepare features and targets
        X = df[self.feature_columns]
        y_cpu = df['cpu_percent']
        y_memory = df['memory_percent']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split data
        X_train, X_test, y_cpu_train, y_cpu_test = train_test_split(X_scaled, y_cpu, test_size=0.2, random_state=42)
        _, _, y_memory_train, y_memory_test = train_test_split(X_scaled, y_memory, test_size=0.2, random_state=42)
        
        # Train CPU prediction model
        self.model_cpu = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model_cpu.fit(X_train, y_cpu_train)
        
        # Train memory prediction model
        self.model_memory = RandomForestRegressor(n_estimators=100, random_state=42)
        self.model_memory.fit(X_train, y_memory_train)
        
        # Evaluate models
        cpu_pred = self.model_cpu.predict(X_test)
        memory_pred = self.model_memory.predict(X_test)
        
        print(f"CPU Model - R² Score: {r2_score(y_cpu_test, cpu_pred):.3f}")
        print(f"Memory Model - R² Score: {r2_score(y_memory_test, memory_pred):.3f}")
        
        # Save models
        self.save_models()
        
        return df
    
    def generate_synthetic_data(self):
        """Generate synthetic data for demonstration purposes"""
        print("Generating synthetic data for demonstration...")
        
        np.random.seed(42)
        n_samples = 100
        
        # Create synthetic time series data
        timestamps = pd.date_range(start='2024-01-01', periods=n_samples, freq='5min')
        
        data = []
        containers = ['web-test', 'cpu-test', 'memory-test']
        
        for i, ts in enumerate(timestamps):
            for container in containers:
                # Create realistic patterns
                hour = ts.hour
                base_cpu = 20 + 30 * np.sin(hour * np.pi / 12)  # Daily pattern
                base_memory = 40 + 20 * np.sin(hour * np.pi / 12)
                
                # Add container-specific patterns
                if container == 'cpu-test':
                    base_cpu += 40
                elif container == 'memory-test':
                    base_memory += 30
                
                # Add noise
                cpu_percent = max(0, min(100, base_cpu + np.random.normal(0, 10)))
                memory_percent = max(0, min(100, base_memory + np.random.normal(0, 8)))
                
                data.append({
                    'container_name': container,
                    'container_id': f'{container[:8]}',
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory_percent,
                    'memory_usage': memory_percent * 10,  # MB
                    'system_cpu_percent': 50 + np.random.normal(0, 15),
                    'system_memory_percent': 60 + np.random.normal(0, 10),
                    'timestamp': ts
                })
        
        return pd.DataFrame(data)
    
    def predict_resource_usage(self, container_name, hours_ahead=1):
        """Predict future resource usage for a container"""
        if not self.model_cpu or not self.model_memory:
            print("Models not trained. Please run train_models() first.")
            return None
        
        # Create future timestamp
        future_time = datetime.now() + timedelta(hours=hours_ahead)
        
        # Prepare features for prediction
        features = {
            'hour': future_time.hour,
            'day_of_week': future_time.weekday(),
            'minute': future_time.minute,
            'container_encoded': hash(container_name) % 10,  # Simple encoding
            'cpu_lag1': 25.0,  # Default values - in real scenario, use latest values
            'memory_lag1': 45.0,
            'cpu_lag2': 23.0,
            'memory_lag2': 43.0,
            'cpu_rolling_avg': 24.0,
            'memory_rolling_avg': 44.0,
            'system_cpu_percent': 50.0,
            'system_memory_percent': 60.0
        }
        
        # Convert to array and scale
        X = np.array([[features[col] for col in self.feature_columns]])
        X_scaled = self.scaler.transform(X)
        
        # Make predictions
        cpu_pred = self.model_cpu.predict(X_scaled)[0]
        memory_pred = self.model_memory.predict(X_scaled)[0]
        
        return {
            'container_name': container_name,
            'predicted_cpu_percent': max(0, min(100, cpu_pred)),
            'predicted_memory_percent': max(0, min(100, memory_pred)),
            'prediction_time': future_time.isoformat(),
            'hours_ahead': hours_ahead
        }
    
    def generate_optimization_recommendations(self, predictions):
        """Generate resource optimization recommendations"""
        recommendations = []
        
        for pred in predictions:
            cpu_pred = pred['predicted_cpu_percent']
            memory_pred = pred['predicted_memory_percent']
            container = pred['container_name']
            
            # CPU recommendations
            if cpu_pred > 80:
                recommendations.append({
                    'container': container,
                    'type': 'CPU',
                    'action': 'SCALE_UP',
                    'reason': f'High CPU usage predicted: {cpu_pred:.1f}%',
                    'suggested_cpu_limit': '2.0'
                })
            elif cpu_pred < 20:
                recommendations.append({
                    'container': container,
                    'type': 'CPU',
                    'action': 'SCALE_DOWN',
                    'reason': f'Low CPU usage predicted: {cpu_pred:.1f}%',
                    'suggested_cpu_limit': '0.5'
                })
            
            # Memory recommendations
            if memory_pred > 85:
                recommendations.append({
                    'container': container,
                    'type': 'MEMORY',
                    'action': 'SCALE_UP',
                    'reason': f'High memory usage predicted: {memory_pred:.1f}%',
                    'suggested_memory_limit': '2Gi'
                })
            elif memory_pred < 25:
                recommendations.append({
                    'container': container,
                    'type': 'MEMORY',
                    'action': 'SCALE_DOWN',
                    'reason': f'Low memory usage predicted: {memory_pred:.1f}%',
                    'suggested_memory_limit': '512Mi'
                })
        
        return recommendations
    
    def save_models(self):
        """Save trained models to disk"""
        models_dir = os.path.expanduser('~/ai-container-lab/models')
        os.makedirs(models_dir, exist_ok=True)
        
        joblib.dump(self.model_cpu, os.path.join(models_dir, 'cpu_model.pkl'))
        joblib.dump(self.model_memory, os.path.join(models_dir, 'memory_model.pkl'))
        joblib.dump(self.scaler, os.path.join(models_dir, 'scaler.pkl'))
        
        print("Models saved successfully!")
    
    def load_models(self):
        """Load trained models from disk"""
        models_dir = os.path.expanduser('~/ai-container-lab/models')
        
        try:
            self.model_cpu = joblib.load(os.path.join(models_dir, 'cpu_model.pkl'))
            self.model_memory = joblib.load(os.path.join(models_dir, 'memory_model.pkl'))
            self.scaler = joblib.load(os.path.join(models_dir, 'scaler.pkl'))
            print("Models loaded successfully!")
            return True
        except FileNotFoundError:
            print("Models not found. Please train models first.")
            return False
    
    def visualize_predictions(self, predictions):
        """Create visualizations of predictions"""
        if not predictions:
            print("No predictions to visualize")
            return
        
        # Create plots directory
        plots_dir = os.path.expanduser('~/ai-container-lab/plots')
        os.makedirs(plots_dir, exist_ok=True)
        
        # Extract data for plotting
        containers = [p['container_name'] for p in predictions]
        cpu_preds = [p['predicted_cpu_percent'] for p in predictions]
        memory_preds = [p['predicted_memory_percent'] for p in predictions]
        
        # Create subplot
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # CPU predictions
        ax1.bar(containers, cpu_preds, color='skyblue', alpha=0.7)
        ax1.set_title('Predicted CPU Usage')
        ax1.set_ylabel('CPU Percentage')
        ax1.set_ylim(0, 100)
        ax1.tick_params(axis='x', rotation=45)
        
        # Memory predictions
        ax2.bar(containers, memory_preds, color='lightcoral', alpha=0.7)
        ax2.set_title('Predicted Memory Usage')
        ax2.set_ylabel('Memory Percentage')
        ax2.set_ylim(0, 100)
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig(os.path.join(plots_dir, 'resource_predictions.png'), dpi=300, bbox_inches='tight')
        print(f"Visualization saved to {plots_dir}/resource_predictions.png")

def main():
    """Main function to demonstrate the AI optimizer"""
    optimizer = ContainerResourceOptimizer()
    
    # Train models
    print("=== Training AI Models ===")
    optimizer.train_models()
    
    # Make predictions for running containers
    print("\n=== Making Predictions ===")
    containers = ['web-test', 'cpu-test', 'memory-test']
    predictions = []
    
    for container in containers:
        pred = optimizer.predict_resource_usage(container, hours_ahead=1)
        if pred:
            predictions.append(pred)
            print(f"Container: {container}")
            print(f"  Predicted CPU: {pred['predicted_cpu_percent']:.1f}%")
            print(f"  Predicted Memory: {pred['predicted_memory_percent']:.1f}%")
    
    # Generate recommendations
    print("\n=== Optimization Recommendations ===")
    recommendations = optimizer.generate_optimization_recommendations(predictions)
    
    for rec in recommendations:
        print(f"Container: {rec['container']}")
        print(f"  Action: {rec['action']} {rec['type']}")
        print(f"  Reason: {rec['reason']}")
        if 'suggested_cpu_limit' in rec:
            print(f"  Suggested CPU Limit: {rec['suggested_cpu_limit']}")
        if 'suggested_memory_limit' in rec:
            print(f"  Suggested Memory Limit: {rec['suggested_memory_limit']}")
        print()
    
    # Create visualizations
    print("=== Creating Visualizations ===")
    optimizer.visualize_predictions(predictions)
    
    print("AI optimization analysis complete!")

if __name__ == "__main__":
    main()
EOF

chmod +x ~/ai-container-lab/scripts/ai_optimizer.py
Subtask 2.5: Run the AI Optimizer

# Run the AI optimization script
cd ~/ai-container-lab
python3 scripts/ai_optimizer.py

# Check generated outputs
ls -la models/
ls -la plots/
Task 3: Integrate AI-Driven Optimization with Podman

Subtask 3.1: Create Podman Integration Script

# Create Podman integration script
cat > ~/ai-container-lab/scripts/podman_ai_integration.py << 'EOF'
#!/usr/bin/env python3
"""
Podman AI Integration Script
Automatically applies AI-driven optimization recommendations to Podman containers
"""

import subprocess
import json
import time
from ai_optimizer import ContainerResourceOptimizer
import os
import sys

class PodmanAIIntegration:
    def __init__(self):
        self.optimizer = ContainerResourceOptimizer()
        
    def get_running_containers(self):
        """Get list of currently running containers"""
        try:
            result = subprocess.run(['podman', 'ps', '--format', 'json'], 
                                  capture_output=True, text=True, check=True)
            containers = json.loads(result.stdout)
            return [(c['Names'][0], c['Id'][:12]) for c in containers]
        except subprocess.CalledProcessError as e:
            print(f"Error getting containers: {e}")
            return []
    
    def update_container_resources(self, container_name, cpu_limit=None, memory_limit=None):
        """Update container resource limits"""
        print(f"Updating resources for container: {container_name}")
        
        # Note: Podman doesn't support runtime resource updates like Docker
        # This is a simulation of what would happen in a production environment
        # In practice, you would need to recreate the container with new limits
        
        commands = []
        if cpu_limit:
            commands.append(f"--cpus={cpu_limit}")
        if memory_limit:
            commands.append(f"--memory={memory_limit}")
        
        if commands:
            print(f"Would execute: podman update {' '.join(commands)} {container_name}")
            print("Note: Podman requires container recreation for resource limit changes")
            
            # Log the recommendation
            self.log_optimization_action(container_name, cpu_limit, memory_limit)
            return True
        
        return False
    
    def log_optimization_action(self, container_name, cpu_limit, memory_limit):
        """Log optimization actions to file"""
        log_dir = os.path.expanduser('~/ai-container-lab/logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, 'optimization_actions.log')
        
        with open(log_file, 'a') as f:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] Container: {container_name}\n")
            if cpu_limit:
                f.write(f"  - CPU Limit: {cpu_limit}\n")
            if memory_limit:
                f.write(f"  - Memory Limit: {memory_limit}\n")
            f.write("\n")
    
    def apply_recommendations(self, recommendations):
        """Apply optimization recommendations to containers"""
        print("Applying AI optimization recommendations...")
        
        applied_count = 0
        for rec in recommendations:
            container_name = rec['container']
            action = rec['action']
            
            if action == 'SCALE_UP' or action == 'SCALE_DOWN':
                cpu_limit = rec.get('suggested_cpu_limit')
                memory_limit = rec.get('suggested_memory_limit')
                
                if self.update_container_resources(container_name, cpu_limit, memory_limit):
                    applied_count += 1
        
        print(f"Applied {applied_count} optimization recommendations")
        return applied_count
    
    def create_optimized_container_script(self, container_name, recommendations):
        """Create a script to recreate container with optimized settings"""
        scripts_dir = os.path.expanduser('~/ai-container-lab/scripts')
        script_file = os.path.join(scripts_dir, f'recreate_{container_name}.sh')
        
        # Find recommendations for this container
        container_recs = [r for r in recommendations if r['container'] == container_name]
        
        if not container_recs:
            return None
        
        # Get current container info
        try:
            result = subprocess.run(['podman', 'inspect', container_name], 
                                  capture_output=True, text=True, check=True)
            container_info = json.loads(result.stdout)[0]
            
            # Extract current configuration
            config = container_info['Config']
            image = config['Image']
            cmd = ' '.join(config.get('Cmd', []))
            
            # Build optimized run command
            run_cmd = f"podman run -d --name {container_name}_optimized"
            
            # Apply AI recommendations
            for rec in container_recs:
                if rec['type'] == 'CPU' and 'suggested_cpu_limit' in rec:
                    run_cmd += f" --cpus={rec['suggested_cpu_limit']}"
                elif rec['type'] == 'MEMORY' and 'suggested_memory_limit' in rec:
                    run_cmd += f" --memory={rec['suggested_memory_limit']}"
            
            run_cmd += f" {image}"
            if cmd:
                run_cmd += f" {cmd}"
            
            # Create script
            with open(script_file, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write(f"# AI-Optimized container recreation script for {container_name}\n")
                f.write(f"# Generated on {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"echo 'Stopping original container...'\n")
                f.write(f"podman stop {container_name}\n")
                f.write(f"podman rm {container_name}\n\n")
                f.write(f"echo 'Starting optimized container...'\n")
                f.write(f"{run_cmd}\n\n")
                f.write(f"echo 'Optimized container started successfully!'\n")
            
            os.chmod(script_file, 0o755)
            print(f"Created optimization script: {script_file}")
            return script_file
            
        except subprocess.CalledProcessError as e:
            print(f"Error inspecting container {container_name}: {e}")
            return None
    
    def run_optimization_cycle(self):
        """Run a complete optimization cycle"""
        print("=== Starting AI-Powered Container Optimization Cycle ===")
        
        # Load or train models
        if not self.optimizer.load_models():
            print("Training new models...")
            self.optimizer.train_models()
        
        # Get running containers
        containers = self.get_running_containers()
        if not containers:
            print("No running containers found")
            return
        
        print(f"Found {len(containers)} running containers")
        
        # Make predictions for each container
        predictions = []
        for container_name, container_id in containers:
            pred = self
