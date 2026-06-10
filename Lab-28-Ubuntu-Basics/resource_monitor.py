import psutil
import time

def get_system_resources():
    # CPU usage
    cpu_usage = psutil.cpu_percent(interval=1)
    
    # Memory usage
    memory = psutil.virtual_memory()
    memory_usage = memory.percent
    
    # Disk usage (root partition)
    disk = psutil.disk_usage('/')
    disk_usage = disk.percent
    
    return {
        'CPU Usage (%)': cpu_usage,
        'Memory Usage (%)': memory_usage,
        'Disk Usage (%)': disk_usage
    }

if __name__ == "__main__":
    while True:
        resources = get_system_resources()
        print("\nResource Dashboard")
        print("-----------------")
        for key, value in resources.items():
            print(f"{key}: {value}")
        time.sleep(5)  # Refresh every 5 seconds

def check_alerts(resources):
    alerts = []
    if resources['CPU Usage (%)'] > 80:
        alerts.append("High CPU usage!")
    if resources['Memory Usage (%)'] > 80:
        alerts.append("High memory usage!")
    if resources['Disk Usage (%)'] > 80:
        alerts.append("High disk usage!")
    return alerts

if __name__ == "__main__":
    while True:
        resources = get_system_resources()
        alerts = check_alerts(resources)
        
        print("\nResource Dashboard")
        print("-----------------")
        for key, value in resources.items():
            print(f"{key}: {value}")
        
        if alerts:
            print("\nALERTS:")
            for alert in alerts:
                print(f"⚠️ {alert}")
        
        time.sleep(5)

