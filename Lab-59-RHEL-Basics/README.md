Lab 59: Real-time System Performance Monitoring

Objectives

By completing this lab, students will:

Understand how to monitor system performance in real-time using top and htop.
Learn to write a Bash script that logs CPU, memory, and disk usage.
Create a custom alert system to notify administrators when resource thresholds are exceeded.
Prerequisites

Before starting, ensure you have:

Basic familiarity with the Linux command line.
A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
htop installed (if not, we’ll install it in the lab).
Task 1: Monitor System Performance with top and htop

Step 1: Launch the top Command

Open the terminal on your Linux machine.
Run the following command:
top
Expected Output: A dynamic view of running processes, CPU usage, memory consumption, and more.
Key Concepts:
Load Average: Shows system load over 1, 5, and 15 minutes.
%CPU: Percentage of CPU used by each process.
%MEM: Percentage of memory used by each process.
Troubleshooting: If top doesn’t run, ensure your system is operational.
Step 2: Install and Use htop

Install htop (if not pre-installed):
sudo apt update && sudo apt install htop -y
Launch htop:
htop
Expected Output: A color-coded, interactive process viewer.
Key Features:
Use arrow keys to navigate.
Press F6 to sort processes (e.g., by CPU or memory).
Troubleshooting: If installation fails, check internet connectivity.
Task 2: Log CPU, Memory, and Disk Usage with a Script

Step 1: Create a Logging Script

Open a text editor (e.g., nano):
nano system_monitor.sh
Paste the following script:
#!/bin/bash
LOG_FILE="/var/log/system_monitor.log"

while true; do
    DATE=$(date "+%Y-%m-%d %H:%M:%S")
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
    MEM=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2}')
    DISK=$(df -h / | awk 'NR==2{print $5}')
    
    echo "$DATE] CPU: $CPU% | Memory: $MEM | Disk: $DISK" >> $LOG_FILE
    sleep 5
done
Explanation:
top -bn1: Runs top in batch mode for one iteration.
free -m: Displays memory usage in MB.
df -h /: Shows disk usage for the root partition.
sleep 5: Logs every 5 seconds.
Step 2: Make the Script Executable and Run It

Set execute permissions:
chmod +x system_monitor.sh
Run the script (use Ctrl+C to stop):
sudo ./system_monitor.sh
Expected Outcome: A log file (/var/log/system_monitor.log) with periodic system stats.
Troubleshooting: If permission denied, use sudo.
Task 3: Create a Custom Alert System

Step 1: Modify the Script to Add Alerts

Edit system_monitor.sh:
nano system_monitor.sh
Update the script to include alerts:
#!/bin/bash
LOG_FILE="/var/log/system_monitor.log"
ALERT_THRESHOLD=80  # 80% threshold for alerts

while true; do
    DATE=$(date "+%Y-%m-%d %H:%M:%S")
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
    MEM=$(free -m | awk 'NR==2{printf "%.2f", $3*100/$2}')
    DISK=$(df -h / | awk 'NR==2{print $5}' | tr -d '%')
    
    echo "$DATE] CPU: $CPU% | Memory: $MEM% | Disk: $DISK%" >> $LOG_FILE
    
    # Alert logic
    if (( $(echo "$CPU > $ALERT_THRESHOLD" | bc -l) )); then
        echo "ALERT: High CPU usage detected: $CPU%" | sudo tee -a $LOG_FILE
    fi
    if (( $(echo "$MEM > $ALERT_THRESHOLD" | bc -l) )); then
        echo "ALERT: High Memory usage detected: $MEM%" | sudo tee -a $LOG_FILE
    fi
    if [ "$DISK" -gt "$ALERT_THRESHOLD" ]; then
        echo "ALERT: High Disk usage detected: $DISK%" | sudo tee -a $LOG_FILE
    fi
    
    sleep 5
done
Step 2: Test the Alert System

Run the updated script:
sudo ./system_monitor.sh
Simulate high CPU usage (optional):
stress --cpu 1 --timeout 30s
Expected Outcome: Alerts appear in the log file when thresholds are exceeded.
