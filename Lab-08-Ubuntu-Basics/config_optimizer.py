import json
import subprocess
import os
from datetime import datetime

class ConfigOptimizer:
    def __init__(self):
        self.config_changes = []
        self.backup_dir = "/tmp/config_backups"
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """Ensure backup directory exists"""
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def backup_config_file(self, file_path):
        """Backup configuration file before modification"""
        if os.path.exists(file_path):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"{os.path.basename(file_path)}.backup.{timestamp}"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            try:
                subprocess.run(['cp', file_path, backup_path], check=True)
                print(f"Backed up {file_path} to {backup_path}")
                return backup_path
            except subprocess.CalledProcessError as e:
                print(f"Failed to backup {file_path}: {e}")
                return None
        return None
    
    def apply_cpu_optimization(self, recommendation):
        """Apply CPU-related optimizations"""
        print(f"Applying CPU optimization: {recommendation['recommendation']}")
        
        if "performance mode" in recommendation['config_change']:
            # Set CPU governor to performance
            try:
                # Check available governors
                result = subprocess.run(['cat', '/sys/devices/system/cpu/cpu0/cpufreq/scaling_available_governors'], 
                                      capture_output=True, text=True)
                if result.returncode == 0 and 'performance' in result.stdout:
                    # Apply to all CPUs
                    cpu_count = int(subprocess.run(['nproc'], capture_output=True, text=True).stdout.strip())
                    for cpu in range(cpu_count):
                        gov_file = f'/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_governor'
                        if os.path.exists(gov_file):
                            subprocess.run(['sudo', 'sh', '-c', f'echo performance > {gov_file}'], check=True)
                    
                    self.config_changes.append({
                        'type': 'CPU Governor',
                        'change': 'Set to performance mode',
                        'timestamp': datetime.now().isoformat()
                    })
                    print("CPU governor set to performance mode")
                else:
                    print("Performance governor not available")
            except Exception as e:
                print(f"Failed to set CPU governor: {e}")
        
        elif "powersave mode" in recommendation['config_change']:
            # Set CPU governor to powersave
            try:
                cpu_count = int(subprocess.run(['nproc'], capture_output=True, text=True).stdout.strip())
                for cpu in range(cpu_count):
                    gov_file = f'/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_governor'
                    if os.path.exists(gov_file):
                        subprocess.run(['sudo', 'sh', '-c', f'echo powersave > {gov_file}'], check=True)
                
                self.config_changes.append({
                    'type': 'CPU Governor',
                    'change': 'Set to powersave mode',
                    'timestamp': datetime.now().isoformat()
                })
                print("CPU governor set to powersave mode")
            except Exception as e:
                print(f"Failed to set CPU governor: {e}")
    
    def apply_memory_optimization(self, recommendation):
        """Apply memory-related optimizations"""
        print(f"Applying memory optimization: {recommendation['recommendation']}")
        
        if "swap space" in recommendation['config_change']:
            # Check current swap
            try:
                result = subprocess.run(['swapon', '--show'], capture_output=True, text=True)
                print(f"Current swap configuration:\n{result.stdout}")
                
                # Create additional swap file if needed
                swap_file = '/tmp/additional_swap'
                if not os.path.exists(swap_file):
                    print("Creating additional swap file (1GB)...")
                    subprocess.run(['sudo', 'fallocate', '-l', '1G', swap_file], check=True)
                    subprocess.run(['sudo', 'chmod', '600', swap_file], check=True)
                    subprocess.run(['sudo', 'mkswap', swap_file], check=True)
                    subprocess.run(['sudo', 'swapon', swap_file], check=True)
                    
                    self.config_changes.append({
                        'type': 'Swap Configuration',
                        'change': f'Added 1GB swap file at {swap_file}',
                        'timestamp': datetime.now().isoformat()
                    })
                    print(f"Additional swap file created and activated: {swap_file}")
                
            except Exception as e:
                print(f"Failed to configure swap: {e}")
        
        elif "memory allocation" in recommendation['config_change']:
            # Adjust vm settings for better memory management
            try:
                sysctl_configs = [
                    ('vm.swappiness', '10'),  # Reduce swap usage
                    ('vm.vfs_cache_pressure', '50'),  # Reduce cache pressure
                    ('vm.dirty_ratio', '15'),  # Adjust dirty page ratio
                ]
                
                for param, value in sysctl_configs:
                    subprocess.run(['sudo', 'sysctl', f'{param}={value}'], check=True)
                    print(f"Set {param} = {value}")
                
                self.config_changes.append({
                    'type': 'Memory Management',
                    'change': 'Optimized vm parameters',
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                print(f"Failed to configure memory settings: {e}")
    
    def apply_monitoring_optimization(self, recommendation):
        """Apply monitoring and alerting optimizations"""
        print(f"Applying monitoring optimization: {recommendation['recommendation']}")
        
        # Create a simple monitoring script
        monitor_script = """#!/bin/bash
# AI-Generated System Monitor
LOG_FILE="/var/log/ai_system_monitor.log"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    MEM_USAGE=$(free | grep Mem | awk '{printf("%.1f", $3/$2 * 100.0)}')
    LOAD_AVG=$(uptime | awk -F'load average:' '{print $2}' | cut -d',' -f1 | xargs)
    
    echo "$TIMESTAMP - CPU: ${CPU_USAGE}%, Memory: ${MEM_USAGE}%, Load: ${LOAD_AVG}" >> $LOG_FILE
    
    # Alert if CPU > 90% or Memory > 95%
    if (( $(echo "$CPU_USAGE > 90" | bc -l) )) || (( $(echo "$MEM_USAGE > 95" | bc -l) )); then
        echo "$TIMESTAMP - ALERT: High resource usage detected!" >> $LOG_FILE
        logger "AI Monitor Alert: High resource usage - CPU: ${CPU_USAGE}%, Memory: ${MEM_USAGE}%"
    fi
    
    sleep 60
done
"""
        
        try:
            script_path = '/tmp/ai_monitor.sh'
            with open(script_path, 'w') as f:
                f.write(monitor_script)
            
            os.chmod(script_path, 0o755)
            
            self.config_changes.append({
                'type': 'Monitoring',
                'change': f'Created monitoring script at {script_path}',
                'timestamp': datetime.now().isoformat()
            })
            print(f"Monitoring script created: {script_path}")
            print("To start monitoring: nohup /tmp/ai_monitor.sh &")
            
        except Exception as e:
            print(f"Failed to create monitoring script: {e}")
    
    def apply_recommendations(self, insights_file='ai_insights.json'):
        """Apply AI-generated recommendations"""
        try:
            with open(insights_file, 'r') as f:
                insights = json.load(f)
            
            recommendations = insights.get('recommendations', [])
            
            if not recommendations:
                print("No recommendations found to apply")
                return
            
            print(f"Applying {len(recommendations)} recommendations...")
            
            for rec in recommendations:
                category = rec['category'].lower()
                
                if category == 'cpu':
                    self.apply_cpu_optimization(rec)
                elif category == 'memory':
                    self.apply_memory_optimization(rec)
                elif category == 'anomaly':
                    self.apply_monitoring_optimization(rec)
                else:
                    print(f"Unknown recommendation category: {category}")
            
            # Save applied changes
            self.save_changes_log()
            
        except FileNotFoundError:
            print(f"Insights file {insights_file} not found")
        except Exception as e:
            print(f"Error applying recommendations: {e}")
    
    def save_changes_log(self):
        """Save log of applied changes"""
        log_file = 'applied_optimizations.json'
        with open(log_file, 'w') as f:
            json.dump(self.config_changes, f, indent=2)
        print(f"Applied changes logged to {log_file}")
    
    def rollback_changes(self):
        """Rollback applied changes"""
        print("Rolling back configuration changes...")
        
        # This is a simplified rollback - in production, you'd want more sophisticated rollback
        try:
            # Reset CPU governors to default
            cpu_count = int(subprocess.run(['nproc'], capture_output=True, text=True).stdout.strip())
            for cpu in range(cpu_count):
                gov_file = f'/sys/devices/system/cpu/cpu{cpu}/cpufreq/scaling_governor'
        try:
            if os.path.exists(self.backup_dir):
                print("Backup directory exists")
                return True
        except Exception as e:
            print(f"Error: {e}")
            return False



