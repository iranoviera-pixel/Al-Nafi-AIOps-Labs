import psutil
import time
import json
import pandas as pd
from datetime import datetime
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
import warnings
warnings.filterwarnings('ignore')

class SystemMonitor:
    def __init__(self):
        self.metrics_history = []
        self.scaler = StandardScaler()
        
    def collect_metrics(self):
        """Collect comprehensive system metrics"""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Memory metrics
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            # Disk metrics
            disk_usage = psutil.disk_usage('/')
            disk_io = psutil.disk_io_counters()
            
            # Network metrics
            network_io = psutil.net_io_counters()
            
            # Process metrics
            process_count = len(psutil.pids())
            
            # Load average
            load_avg = psutil.getloadavg()
            
            metrics = {
                'timestamp': datetime.now().isoformat(),
                'cpu_percent': cpu_percent,
                'cpu_count': cpu_count,
                'cpu_freq_current': cpu_freq.current if cpu_freq else 0,
                'memory_percent': memory.percent,
                'memory_available': memory.available,
                'memory_used': memory.used,
                'swap_percent': swap.percent,
                'disk_percent': disk_usage.percent,
                'disk_free': disk_usage.free,
                'disk_read_bytes': disk_io.read_bytes if disk_io else 0,
                'disk_write_bytes': disk_io.write_bytes if disk_io else 0,
                'network_bytes_sent': network_io.bytes_sent,
                'network_bytes_recv': network_io.bytes_recv,
                'process_count': process_count,
                'load_avg_1min': load_avg[0],
                'load_avg_5min': load_avg[1],
                'load_avg_15min': load_avg[2]
            }
            
            return metrics
            
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            return None
    
    def collect_continuous_metrics(self, duration_minutes=10, interval_seconds=30):
        """Collect metrics continuously for analysis"""
        print(f"Collecting metrics for {duration_minutes} minutes...")
        
        end_time = time.time() + (duration_minutes * 60)
        
        while time.time() < end_time:
            metrics = self.collect_metrics()
            if metrics:
                self.metrics_history.append(metrics)
                print(f"Collected metrics at {metrics['timestamp']}")
            
            time.sleep(interval_seconds)
        
        print(f"Collection complete. Total samples: {len(self.metrics_history)}")
        return self.metrics_history
    
    def save_metrics(self, filename='system_metrics.json'):
        """Save collected metrics to file"""
        with open(filename, 'w') as f:
            json.dump(self.metrics_history, f, indent=2)
        print(f"Metrics saved to {filename}")

if __name__ == "__main__":
    monitor = SystemMonitor()
    
    # Collect single snapshot
    current_metrics = monitor.collect_metrics()
    print("Current System Metrics:")
    for key, value in current_metrics.items():
        print(f"{key}: {value}")
    
    # Collect continuous metrics (uncomment for longer collection)
    # monitor.collect_continuous_metrics(duration_minutes=5, interval_seconds=10)
    # monitor.save_metrics()

