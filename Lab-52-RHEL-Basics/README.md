Lab 52: Using top, vmstat, and iostat for System Monitoring

Objectives

By the end of this lab, you will be able to:

Use the top command to monitor real-time CPU and memory usage
Utilize vmstat to analyze memory, processes, and paging statistics
Apply iostat to examine disk I/O performance metrics
Create automated monitoring scripts for continuous system observation
Interpret system performance data to identify potential bottlenecks
Understand the relationship between CPU, memory, and disk performance
Prerequisites

Before starting this lab, you should have:

Basic knowledge of Linux command line interface
Understanding of fundamental system concepts (CPU, memory, disk)
Familiarity with text editors like nano or vim
Basic shell scripting knowledge (variables, loops, conditionals)
Lab Environment Setup

Al Nafi Cloud Machines: This lab uses Linux-based cloud machines provided by Al Nafi. Simply click Start Lab to access your pre-configured environment. No need to build your own virtual machine or install additional software.

Your cloud machine comes with:

Ubuntu Linux operating system
All required monitoring tools pre-installed
Root access for system monitoring
Sample workloads for testing
Task 1: Using top for CPU and Memory Monitoring

Subtask 1.1: Basic top Command Usage

The top command provides a real-time view of running processes and system resource usage.

Open your terminal in the cloud machine

Run the basic top command:

top
Observe the output sections:

System summary (first 5 lines): uptime, users, load average, tasks, CPU usage
Memory information: total, free, used, buffer/cache
Process list: PID, user, priority, CPU%, memory%, command
Press q to quit top

Subtask 1.2: Understanding top Output

Run top again and focus on the header information:
top
Identify key metrics:

Load average: System load over 1, 5, and 15 minutes
CPU usage: User space, system, idle, wait, hardware interrupts
Memory usage: Total, free, used, buffers, cached
Note the process information columns:

PID: Process ID
USER: Process owner
PR: Priority
%CPU: CPU usage percentage
%MEM: Memory usage percentage
COMMAND: Process name
Subtask 1.3: Interactive top Commands

While top is running, try these interactive commands:

Sort by memory usage:

Press 'M' (capital M)
Sort by CPU usage:
Press 'P' (capital P)
Filter processes by user:
Press 'u' then type username (e.g., root)
Change update interval to 2 seconds:
Press 's' then type '2'
Kill a process (be careful):
Press 'k' then enter PID number
Subtask 1.4: top Command Options

Run top with specific options:

Show only specific user processes:

top -u root
Run top in batch mode (non-interactive):
top -b -n 1
Display specific number of processes:
top -n 1 | head -20
Task 2: Using vmstat for Memory and Process Statistics

Subtask 2.1: Basic vmstat Usage

The vmstat command reports virtual memory statistics including processes, memory, paging, block IO, and CPU activity.

Run basic vmstat command:
vmstat
Understand the output columns:
procs: r (running), b (blocked)
memory: swpd (swap), free, buff (buffers), cache
swap: si (swap in), so (swap out)
io: bi (blocks in), bo (blocks out)
system: in (interrupts), cs (context switches)
cpu: us (user), sy (system), id (idle), wa (wait)
Subtask 2.2: Continuous Monitoring with vmstat

Monitor system every 2 seconds for 10 intervals:
vmstat 2 10
Generate some system load to see changes:
# Open another terminal and run:
dd if=/dev/zero of=/tmp/testfile bs=1M count=100
While the dd command runs, observe vmstat output changes in:
CPU usage (us, sy, wa columns)
I/O activity (bi, bo columns)
Memory usage (free, cache columns)
Subtask 2.3: Memory-Specific vmstat Options

Display memory statistics in megabytes:
vmstat -S M
Show detailed memory statistics:
vmstat -s
Display disk statistics:
vmstat -d
Subtask 2.4: Creating System Load for Testing

Create a script to generate CPU load:
nano cpu_load.sh
Add the following content:
#!/bin/bash
# CPU load generator
echo "Generating CPU load for 30 seconds..."
timeout 30s yes > /dev/null &
timeout 30s yes > /dev/null &
timeout 30s yes > /dev/null &
wait
echo "CPU load test completed"
Make the script executable and run it:
chmod +x cpu_load.sh
./cpu_load.sh
In another terminal, monitor with vmstat:
vmstat 1 35
Task 3: Using iostat for Disk I/O Statistics

Subtask 3.1: Installing and Basic iostat Usage

Install sysstat package (if not already installed):
sudo apt update
sudo apt install sysstat -y
Run basic iostat command:
iostat
Understand the output:
Device: Storage device name
tps: Transfers per second
kB_read/s: Kilobytes read per second
kB_wrtn/s: Kilobytes written per second
kB_read: Total kilobytes read
kB_wrtn: Total kilobytes written
Subtask 3.2: Extended iostat Monitoring

Display extended statistics:
iostat -x
Monitor continuously every 2 seconds:
iostat -x 2
Show statistics for specific device:
iostat -x /dev/sda 2 5
Subtask 3.3: Generating Disk I/O Load

Create a script to generate disk I/O:
nano disk_io_test.sh
Add the following content:
#!/bin/bash
# Disk I/O load generator
echo "Generating disk I/O load..."

# Create test directory
mkdir -p /tmp/iostest
cd /tmp/iostest

# Generate write load
echo "Writing test files..."
for i in {1..5}; do
    dd if=/dev/zero of=testfile$i bs=1M count=50 2>/dev/null &
done
wait

# Generate read load
echo "Reading test files..."
for i in {1..5}; do
    dd if=testfile$i of=/dev/null bs=1M 2>/dev/null &
done
wait

# Cleanup
rm -f testfile*
cd /
rmdir /tmp/iostest

echo "Disk I/O test completed"
Make executable and run:
chmod +x disk_io_test.sh
./disk_io_test.sh
Monitor I/O during the test:
iostat -x 1
Subtask 3.4: Advanced iostat Options

Display statistics in megabytes:
iostat -m
Show CPU and device statistics:
iostat -c -d 2 5
Display network filesystem statistics:
iostat -n
Task 4: Creating Automated System Monitoring Scripts

Subtask 4.1: Basic Monitoring Script

Create a comprehensive monitoring script:
nano system_monitor.sh
Add the following content:
#!/bin/bash
# Comprehensive System Monitoring Script

# Configuration
INTERVAL=5
DURATION=60
LOG_FILE="/tmp/system_monitor.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Function to log with timestamp
log_with_timestamp() {
    echo "[$TIMESTAMP] $1" >> $LOG_FILE
}

# Function to monitor CPU and memory
monitor_cpu_memory() {
    echo "=== CPU and Memory Monitoring ===" >> $LOG_FILE
    top -b -n 1 | head -20 >> $LOG_FILE
    echo "" >> $LOG_FILE
}

# Function to monitor memory statistics
monitor_memory_stats() {
    echo "=== Memory Statistics ===" >> $LOG_FILE
    vmstat 1 1 >> $LOG_FILE
    echo "" >> $LOG_FILE
}

# Function to monitor disk I/O
monitor_disk_io() {
    echo "=== Disk I/O Statistics ===" >> $LOG_FILE
    iostat -x 1 1 >> $LOG_FILE
    echo "" >> $LOG_FILE
}

# Main monitoring loop
echo "Starting system monitoring..."
echo "Log file: $LOG_FILE"
echo "Monitoring interval: $INTERVAL seconds"
echo "Duration: $DURATION seconds"

# Initialize log file
echo "System Monitoring Started at $TIMESTAMP" > $LOG_FILE
echo "=========================================" >> $LOG_FILE

# Calculate number of iterations
ITERATIONS=$((DURATION / INTERVAL))

for i in $(seq 1 $ITERATIONS); do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    log_with_timestamp "Monitoring iteration $i of $ITERATIONS"
    
    monitor_cpu_memory
    monitor_memory_stats
    monitor_disk_io
    
    echo "----------------------------------------" >> $LOG_FILE
    
    if [ $i -lt $ITERATIONS ]; then
        sleep $INTERVAL
    fi
done

echo "Monitoring completed. Check log file: $LOG_FILE"
Make the script executable:
chmod +x system_monitor.sh
Subtask 4.2: Advanced Monitoring Script with Alerts

Create an advanced monitoring script with alert thresholds:
nano advanced_monitor.sh
Add the following content:
#!/bin/bash
# Advanced System Monitoring with Alerts

# Configuration
INTERVAL=10
CPU_THRESHOLD=80
MEMORY_THRESHOLD=80
DISK_IO_THRESHOLD=100
LOG_FILE="/tmp/advanced_monitor.log"
ALERT_FILE="/tmp/system_alerts.log"

# Function to check CPU usage
check_cpu_usage() {
    CPU_USAGE=$(top -b -n 1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
    CPU_USAGE=${CPU_USAGE%.*}  # Remove decimal part
    
    if [ "$CPU_USAGE" -gt "$CPU_THRESHOLD" ]; then
        ALERT="HIGH CPU USAGE: ${CPU_USAGE}% (Threshold: ${CPU_THRESHOLD}%)"
        echo "[$(date)] $ALERT" >> $ALERT_FILE
        echo "ALERT: $ALERT"
    fi
    
    echo "CPU Usage: ${CPU_USAGE}%" >> $LOG_FILE
}

# Function to check memory usage
check_memory_usage() {
    MEMORY_INFO=$(free | grep Mem)
    TOTAL_MEM=$(echo $MEMORY_INFO | awk '{print $2}')
    USED_MEM=$(echo $MEMORY_INFO | awk '{print $3}')
    MEMORY_USAGE=$((USED_MEM * 100 / TOTAL_MEM))
    
    if [ "$MEMORY_USAGE" -gt "$MEMORY_THRESHOLD" ]; then
        ALERT="HIGH MEMORY USAGE: ${MEMORY_USAGE}% (Threshold: ${MEMORY_THRESHOLD}%)"
        echo "[$(date)] $ALERT" >> $ALERT_FILE
        echo "ALERT: $ALERT"
    fi
    
    echo "Memory Usage: ${MEMORY_USAGE}%" >> $LOG_FILE
}

# Function to check disk I/O
check_disk_io() {
    DISK_UTIL=$(iostat -x 1 1 | tail -n +4 | head -1 | awk '{print $NF}')
    DISK_UTIL=${DISK_UTIL%.*}  # Remove decimal part
    
    if [ ! -z "$DISK_UTIL" ] && [ "$DISK_UTIL" -gt "$DISK_IO_THRESHOLD" ]; then
        ALERT="HIGH DISK I/O: ${DISK_UTIL}% utilization (Threshold: ${DISK_IO_THRESHOLD}%)"
        echo "[$(date)] $ALERT" >> $ALERT_FILE
        echo "ALERT: $ALERT"
    fi
    
    echo "Disk Utilization: ${DISK_UTIL}%" >> $LOG_FILE
}

# Main monitoring function
monitor_system() {
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$TIMESTAMP] System Check" >> $LOG_FILE
    
    check_cpu_usage
    check_memory_usage
    check_disk_io
    
    echo "---" >> $LOG_FILE
}

# Initialize log files
echo "Advanced System Monitoring Started at $(date)" > $LOG_FILE
echo "Advanced System Monitoring Alerts Started at $(date)" > $ALERT_FILE

echo "Starting advanced system monitoring..."
echo "CPU Threshold: ${CPU_THRESHOLD}%"
echo "Memory Threshold: ${MEMORY_THRESHOLD}%"
echo "Disk I/O Threshold: ${DISK_IO_THRESHOLD}%"
echo "Check interval: ${INTERVAL} seconds"
echo "Press Ctrl+C to stop monitoring"

# Continuous monitoring loop
while true; do
    monitor_system
    sleep $INTERVAL
done
Make the script executable:
chmod +x advanced_monitor.sh
Subtask 4.3: Running and Testing Monitoring Scripts

Run the basic monitoring script:
./system_monitor.sh
View the generated log:
cat /tmp/system_monitor.log
Run the advanced monitoring script in background:
./advanced_monitor.sh &
Generate some system load to trigger alerts:
# Generate CPU load
yes > /dev/null &
PID1=$!

# Generate memory load
dd if=/dev/zero of=/tmp/bigfile bs=1M count=500 2>/dev/null &
PID2=$!

# Wait a bit then check alerts
sleep 30
cat /tmp/system_alerts.log

# Clean up
kill $PID1 $PID2 2>/dev/null
rm -f /tmp/bigfile
Stop the advanced monitoring:
pkill -f advanced_monitor.sh
Subtask 4.4: Creating a Monitoring Dashboard Script

Create a real-time dashboard script:
nano monitor_dashboard.sh
Add the following content:
#!/bin/bash
# Real-time System Monitoring Dashboard

# Function to clear screen and show header
show_header() {
    clear
    echo "=========================================="
    echo "    SYSTEM MONITORING DASHBOARD"
    echo "=========================================="
    echo "Last Updated: $(date)"
    echo "Press Ctrl+C to exit"
    echo "=========================================="
    echo
}

# Function to show CPU information
show_cpu_info() {
    echo "CPU INFORMATION:"
    echo "----------------"
    top -b -n 1 | grep "Cpu(s)" | sed 's/Cpu(s)://'
    echo
}

# Function to show memory information
show_memory_info() {
    echo "MEMORY INFORMATION:"
    echo "-------------------"
    free -h | grep -E "(Mem|Swap)"
    echo
}

# Function to show disk usage
show_disk_usage() {
    echo "DISK USAGE:"
    echo "-----------"
    df -h | grep -E "(Filesystem|/dev/)"
    echo
}

# Function to show top processes
show_top_processes() {
    echo "TOP 5 CPU PROCESSES:"
    echo "--------------------"
    ps aux --sort=-%cpu | head -6 | awk '{printf "%-10s %-6s %-6s %s\n", $1, $2, $3, $11}'
    echo
}

# Function to show I/O statistics
show_io_stats() {
    echo "DISK I/O STATISTICS:"
    echo "--------------------"
    iostat -x 1 1 | tail -n +4 | head -3
    echo
}

# Main dashboard loop
while true; do
    show_header
    show_cpu_info
    show_memory_info
    show_disk_usage
    show_top_processes
    show_io_stats
    
    sleep 5
done
Make executable and run:
chmod +x monitor_dashboard.sh
./monitor_dashboard.sh
