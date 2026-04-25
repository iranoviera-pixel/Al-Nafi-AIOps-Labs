import psutil
import subprocess

def adjust_priority(pid, priority):
    try:
        subprocess.run(['renice', str(priority), str(pid)], check=True)
        print(f"Adjusted priority for PID {pid} to {priority}")
    except subprocess.CalledProcessError as e:
        print(f"Error adjusting priority: {e}")

# Example: Find top CPU process and adjust
for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
    if proc.info['cpu_percent'] > 80:  # If process uses >80% CPU
        adjust_priority(proc.info['pid'], 19)  # Lowest priority


