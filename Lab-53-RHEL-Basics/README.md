Lab 53: Introduction to Performance Co-Pilot (PCP)

Lab Objectives

By the end of this lab, students will be able to:

Understand the fundamentals of Performance Co-Pilot (PCP) and its role in system monitoring
Install and configure PCP on a Linux system
Use pmchart to visualize system performance metrics in real-time
Utilize pmie (Performance Metrics Inference Engine) to analyze performance data
Create automated scripts for collecting and reporting system performance metrics
Interpret performance data to identify system bottlenecks and optimization opportunities
Prerequisites

Before starting this lab, students should have:

Basic understanding of Linux command line operations
Familiarity with system administration concepts
Knowledge of basic system performance metrics (CPU, memory, disk I/O)
Understanding of shell scripting fundamentals
Access to a terminal or command prompt
Lab Environment Setup

Ready-to-Use Cloud Machines: Al Nafi provides pre-configured Linux-based cloud machines for this lab. Simply click Start Lab to access your dedicated environment. No need to build your own virtual machine or worry about initial setup configurations.

Your cloud machine comes with:

Ubuntu 20.04 LTS or CentOS 8
Root access privileges
Internet connectivity for package installation
Pre-installed development tools
Task 1: Install and Configure Performance Co-Pilot (PCP)

Subtask 1.1: Update System Packages

First, ensure your system packages are up to date:

# For Ubuntu/Debian systems
sudo apt update && sudo apt upgrade -y

# For CentOS/RHEL systems
sudo yum update -y
Subtask 1.2: Install PCP Core Components

Install the main PCP packages:

# For Ubuntu/Debian systems
sudo apt install -y pcp pcp-gui pcp-import-sar2pcp pcp-import-iostat2pcp

# For CentOS/RHEL systems
sudo yum install -y pcp pcp-gui pcp-import-sar2pcp pcp-import-iostat2pcp
Subtask 1.3: Start and Enable PCP Services

Enable and start the PCP collector daemon:

# Start the PCP collector daemon
sudo systemctl start pmcd

# Enable it to start automatically on boot
sudo systemctl enable pmcd

# Check the status
sudo systemctl status pmcd
Subtask 1.4: Verify PCP Installation

Verify that PCP is working correctly:

# Check PCP version
pcp --version

# List available performance metrics
pminfo | head -20

# Check system information
pcp summary
Subtask 1.5: Configure PCP Logging

Enable performance metric logging:

# Start the PCP logger daemon
sudo systemctl start pmlogger

# Enable it for automatic startup
sudo systemctl enable pmlogger

# Verify logger status
sudo systemctl status pmlogger
Task 2: Use pmchart and pmie to View and Analyze Performance Metrics

Subtask 2.1: Introduction to pmchart

pmchart is a graphical tool for real-time visualization of PCP performance metrics.

First, let's explore basic pmchart functionality:

# Launch pmchart (if GUI is available)
pmchart &

# For command-line environments, use pmval for real-time metrics
pmval -t 2 kernel.all.load
Subtask 2.2: Monitor CPU Performance

Create a script to monitor CPU metrics:

# Create a CPU monitoring script
cat > cpu_monitor.sh << 'EOF'
#!/bin/bash

echo "=== CPU Performance Monitoring ==="
echo "Date: $(date)"
echo

# Display current CPU load
echo "Current CPU Load Average:"
pmval -s 1 kernel.all.load

echo
echo "CPU Utilization by State:"
pmval -s 5 -t 1 kernel.all.cpu.user kernel.all.cpu.sys kernel.all.cpu.idle

echo
echo "Per-CPU Statistics:"
pmval -s 3 -t 2 kernel.percpu.cpu.user kernel.percpu.cpu.sys
EOF

chmod +x cpu_monitor.sh
./cpu_monitor.sh
Subtask 2.3: Monitor Memory Performance

Create a memory monitoring script:

# Create a memory monitoring script
cat > memory_monitor.sh << 'EOF'
#!/bin/bash

echo "=== Memory Performance Monitoring ==="
echo "Date: $(date)"
echo

# Display memory usage
echo "Memory Usage Summary:"
pmval -s 1 mem.util.used mem.util.free mem.util.available

echo
echo "Memory Statistics (MB):"
pmval -s 3 -t 2 mem.physmem mem.util.used mem.util.bufmem mem.util.cached

echo
echo "Swap Usage:"
pmval -s 1 swap.used swap.free
EOF

chmod +x memory_monitor.sh
./memory_monitor.sh
Subtask 2.4: Monitor Disk I/O Performance

Create a disk I/O monitoring script:

# Create a disk I/O monitoring script
cat > disk_monitor.sh << 'EOF'
#!/bin/bash

echo "=== Disk I/O Performance Monitoring ==="
echo "Date: $(date)"
echo

# Display disk I/O statistics
echo "Disk I/O Operations:"
pmval -s 5 -t 1 disk.all.read disk.all.write

echo
echo "Disk I/O Bytes:"
pmval -s 5 -t 1 disk.all.read_bytes disk.all.write_bytes

echo
echo "Disk Utilization:"
pmval -s 3 -t 2 disk.all.avactive
EOF

chmod +x disk_monitor.sh
./disk_monitor.sh
Subtask 2.5: Introduction to pmie (Performance Metrics Inference Engine)

pmie is used to create rules that monitor performance metrics and trigger actions based on conditions.

Create a basic pmie configuration:

# Create a pmie rules file
cat > system_alerts.pmie << 'EOF'
// High CPU usage alert
some_host (
    kernel.all.cpu.user + kernel.all.cpu.sys > 80
) -> print "HIGH CPU USAGE: %v%% at %t";

// High memory usage alert
some_host (
    100 * mem.util.used / mem.physmem > 90
) -> print "HIGH MEMORY USAGE: %v%% at %t";

// High load average alert
some_host (
    kernel.all.load #'1 minute' > 4
) -> print "HIGH LOAD AVERAGE: %v at %t";

// Low disk space alert (if available)
some_host (
    filesys.free < 1024
) -> print "LOW DISK SPACE: %v MB free at %t";
EOF
Test the pmie configuration:

# Test the pmie rules
pmie -T 30 -t 5 system_alerts.pmie
Task 3: Write a Script to Automate Collection and Reporting of System Performance Metrics

Subtask 3.1: Create a Comprehensive Performance Collection Script

Create an advanced script that collects multiple performance metrics:

# Create the main performance collection script
cat > performance_collector.sh << 'EOF'
#!/bin/bash

# Performance Collector Script using PCP
# This script collects and reports system performance metrics

# Configuration
REPORT_DIR="/tmp/pcp_reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="$REPORT_DIR/performance_report_$TIMESTAMP.txt"
DURATION=60  # Collection duration in seconds
INTERVAL=5   # Sample interval in seconds

# Create report directory
mkdir -p "$REPORT_DIR"

# Function to print header
print_header() {
    echo "========================================" >> "$REPORT_FILE"
    echo "$1" >> "$REPORT_FILE"
    echo "Time: $(date)" >> "$REPORT_FILE"
    echo "========================================" >> "$REPORT_FILE"
    echo >> "$REPORT_FILE"
}

# Function to collect CPU metrics
collect_cpu_metrics() {
    print_header "CPU PERFORMANCE METRICS"
    
    echo "CPU Load Average:" >> "$REPORT_FILE"
    pmval -s 1 kernel.all.load >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
    
    echo "CPU Utilization (%):" >> "$REPORT_FILE"
    pmval -s 12 -t 5 kernel.all.cpu.user kernel.all.cpu.sys kernel.all.cpu.idle >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
    
    echo "Context Switches per second:" >> "$REPORT_FILE"
    pmval -s 6 -t 10 kernel.all.pswitch >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
}

# Function to collect memory metrics
collect_memory_metrics() {
    print_header "MEMORY PERFORMANCE METRICS"
    
    echo "Memory Usage (MB):" >> "$REPORT_FILE"
    pmval -s 1 mem.physmem mem.util.used mem.util.free mem.util.available >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
    
    echo "Memory Utilization Over Time:" >> "$REPORT_FILE"
    pmval -s 12 -t 5 mem.util.used mem.util.cached mem.util.bufmem >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
    
    echo "Swap Usage:" >> "$REPORT_FILE"
    pmval -s 1 swap.used swap.free >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
}

# Function to collect disk I/O metrics
collect_disk_metrics() {
    print_header "DISK I/O PERFORMANCE METRICS"
    
    echo "Disk I/O Operations:" >> "$REPORT_FILE"
    pmval -s 12 -t 5 disk.all.read disk.all.write >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
    
    echo "Disk I/O Throughput (Bytes):" >> "$REPORT_FILE"
    pmval -s 12 -t 5 disk.all.read_bytes disk.all.write_bytes >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
    
    echo "Average Disk Utilization:" >> "$REPORT_FILE"
    pmval -s 6 -t 10 disk.all.avactive >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
}

# Function to collect network metrics
collect_network_metrics() {
    print_header "NETWORK PERFORMANCE METRICS"
    
    echo "Network Interface Statistics:" >> "$REPORT_FILE"
    pmval -s 6 -t 10 network.interface.in.bytes network.interface.out.bytes >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
    
    echo "Network Packets:" >> "$REPORT_FILE"
    pmval -s 6 -t 10 network.interface.in.packets network.interface.out.packets >> "$REPORT_FILE" 2>/dev/null
    echo >> "$REPORT_FILE"
}

# Function to generate summary
generate_summary() {
    print_header "PERFORMANCE SUMMARY"
    
    echo "System Information:" >> "$REPORT_FILE"
    echo "Hostname: $(hostname)" >> "$REPORT_FILE"
    echo "Kernel: $(uname -r)" >> "$REPORT_FILE"
    echo "Uptime: $(uptime)" >> "$REPORT_FILE"
    echo >> "$REPORT_FILE"
    
    echo "Collection Parameters:" >> "$REPORT_FILE"
    echo "Duration: $DURATION seconds" >> "$REPORT_FILE"
    echo "Interval: $INTERVAL seconds" >> "$REPORT_FILE"
    echo "Report File: $REPORT_FILE" >> "$REPORT_FILE"
    echo >> "$REPORT_FILE"
}

# Main execution
echo "Starting performance data collection..."
echo "Report will be saved to: $REPORT_FILE"

# Generate report header
echo "SYSTEM PERFORMANCE REPORT" > "$REPORT_FILE"
echo "Generated on: $(date)" >> "$REPORT_FILE"
echo "=============================================" >> "$REPORT_FILE"
echo >> "$REPORT_FILE"

# Collect all metrics
generate_summary
collect_cpu_metrics
collect_memory_metrics
collect_disk_metrics
collect_network_metrics

# Final message
print_header "COLLECTION COMPLETE"
echo "Performance data collection completed successfully." >> "$REPORT_FILE"
echo "Total samples collected over $DURATION seconds." >> "$REPORT_FILE"

echo "Performance data collection completed!"
echo "Report saved to: $REPORT_FILE"
echo
echo "To view the report:"
echo "cat $REPORT_FILE"
EOF

chmod +x performance_collector.sh
Subtask 3.2: Create a Performance Analysis Script

Create a script that analyzes the collected performance data:

# Create performance analysis script
cat > performance_analyzer.sh << 'EOF'
#!/bin/bash

# Performance Analyzer Script
# Analyzes PCP performance data and provides recommendations

ANALYSIS_FILE="/tmp/pcp_reports/performance_analysis_$(date +%Y%m%d_%H%M%S).txt"

# Function to analyze CPU performance
analyze_cpu() {
    echo "=== CPU ANALYSIS ===" >> "$ANALYSIS_FILE"
    
    # Get current CPU load
    LOAD_1MIN=$(pmval -s 1 kernel.all.load | tail -1 | awk '{print $2}')
    CPU_COUNT=$(nproc)
    
    echo "Current 1-minute load average: $LOAD_1MIN" >> "$ANALYSIS_FILE"
    echo "Number of CPU cores: $CPU_COUNT" >> "$ANALYSIS_FILE"
    
    # Calculate load per core
    LOAD_PER_CORE=$(echo "scale=2; $LOAD_1MIN / $CPU_COUNT" | bc 2>/dev/null || echo "N/A")
    echo "Load per core: $LOAD_PER_CORE" >> "$ANALYSIS_FILE"
    
    # Provide recommendations
    if (( $(echo "$LOAD_1MIN > $CPU_COUNT" | bc -l 2>/dev/null || echo 0) )); then
        echo "RECOMMENDATION: High CPU load detected. Consider optimizing processes or adding CPU resources." >> "$ANALYSIS_FILE"
    else
        echo "CPU load is within normal range." >> "$ANALYSIS_FILE"
    fi
    echo >> "$ANALYSIS_FILE"
}

# Function to analyze memory performance
analyze_memory() {
    echo "=== MEMORY ANALYSIS ===" >> "$ANALYSIS_FILE"
    
    # Get memory statistics
    TOTAL_MEM=$(pmval -s 1 mem.physmem | tail -1 | awk '{print $2}')
    USED_MEM=$(pmval -s 1 mem.util.used | tail -1 | awk '{print $2}')
    
    if [ "$TOTAL_MEM" != "" ] && [ "$USED_MEM" != "" ]; then
        MEMORY_USAGE=$(echo "scale=2; ($USED_MEM / $TOTAL_MEM) * 100" | bc 2>/dev/null || echo "N/A")
        echo "Total Memory: $TOTAL_MEM KB" >> "$ANALYSIS_FILE"
        echo "Used Memory: $USED_MEM KB" >> "$ANALYSIS_FILE"
        echo "Memory Usage: $MEMORY_USAGE%" >> "$ANALYSIS_FILE"
        
        # Provide recommendations
        if (( $(echo "$MEMORY_USAGE > 90" | bc -l 2>/dev/null || echo 0) )); then
            echo "RECOMMENDATION: High memory usage detected. Consider freeing memory or adding RAM." >> "$ANALYSIS_FILE"
        elif (( $(echo "$MEMORY_USAGE > 75" | bc -l 2>/dev/null || echo 0) )); then
            echo "RECOMMENDATION: Moderate memory usage. Monitor for potential issues." >> "$ANALYSIS_FILE"
        else
            echo "Memory usage is within acceptable range." >> "$ANALYSIS_FILE"
        fi
    else
        echo "Unable to retrieve memory statistics." >> "$ANALYSIS_FILE"
    fi
    echo >> "$ANALYSIS_FILE"
}

# Function to analyze disk performance
analyze_disk() {
    echo "=== DISK I/O ANALYSIS ===" >> "$ANALYSIS_FILE"
    
    # Get disk I/O statistics
    echo "Recent Disk I/O Activity:" >> "$ANALYSIS_FILE"
    pmval -s 3 -t 2 disk.all.read disk.all.write >> "$ANALYSIS_FILE" 2>/dev/null
    
    echo "RECOMMENDATION: Monitor disk I/O patterns for bottlenecks during peak usage." >> "$ANALYSIS_FILE"
    echo >> "$ANALYSIS_FILE"
}

# Function to generate recommendations
generate_recommendations() {
    echo "=== GENERAL RECOMMENDATIONS ===" >> "$ANALYSIS_FILE"
    echo "1. Regularly monitor system performance using PCP tools" >> "$ANALYSIS_FILE"
    echo "2. Set up automated alerts using pmie for critical thresholds" >> "$ANALYSIS_FILE"
    echo "3. Archive performance data for historical analysis" >> "$ANALYSIS_FILE"
    echo "4. Use pmchart for real-time visualization when GUI is available" >> "$ANALYSIS_FILE"
    echo "5. Consider implementing performance baselines for comparison" >> "$ANALYSIS_FILE"
    echo >> "$ANALYSIS_FILE"
}

# Main execution
echo "PERFORMANCE ANALYSIS REPORT" > "$ANALYSIS_FILE"
echo "Generated on: $(date)" >> "$ANALYSIS_FILE"
echo "===============================" >> "$ANALYSIS_FILE"
echo >> "$ANALYSIS_FILE"

analyze_cpu
analyze_memory
analyze_disk
generate_recommendations

echo "Performance analysis completed!"
echo "Analysis report saved to: $ANALYSIS_FILE"
echo
echo "To view the analysis:"
echo "cat $ANALYSIS_FILE"
EOF

chmod +x performance_analyzer.sh
Subtask 3.3: Create an Automated Monitoring Script

Create a script that runs continuous monitoring:

# Create automated monitoring script
cat > automated_monitor.sh << 'EOF'
#!/bin/bash

# Automated Performance Monitoring Script
# Runs continuous monitoring and generates alerts

MONITOR_DIR="/tmp/pcp_monitoring"
LOG_FILE="$MONITOR_DIR/monitor.log"
ALERT_FILE="$MONITOR_DIR/alerts.log"

# Create monitoring directory
mkdir -p "$MONITOR_DIR"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Function to check CPU load
check_cpu_load() {
    LOAD_1MIN=$(pmval -s 1 kernel.all.load 2>/dev/null | tail -1 | awk '{print $2}')
    CPU_COUNT=$(nproc)
    
    if [ "$LOAD_1MIN" != "" ] && [ "$CPU_COUNT" != "" ]; then
        if (( $(echo "$LOAD_1MIN > ($CPU_COUNT * 2)" | bc -l 2>/dev/null || echo 0) )); then
            ALERT="HIGH CPU LOAD: $LOAD_1MIN (Cores: $CPU_COUNT)"
            log_message "$ALERT"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] $ALERT" >> "$ALERT_FILE"
        fi
    fi
}

# Function to check memory usage
check_memory_usage() {
    TOTAL_MEM=$(pmval -s 1 mem.physmem 2>/dev/null | tail -1 | awk '{print $2}')
    USED_MEM=$(pmval -s 1 mem.util.used 2>/dev/null | tail -1 | awk '{print $2}')
    
    if [ "$TOTAL_MEM" != "" ] && [ "$USED_MEM" != "" ]; then
        MEMORY_USAGE=$(echo "scale=2; ($USED_MEM / $TOTAL_MEM) * 100" | bc 2>/dev/null)
        if [ "$MEMORY_USAGE" != "" ] && (( $(echo "$MEMORY_USAGE > 90" | bc -l 2>/dev/null || echo 0) )); then
            ALERT="HIGH MEMORY USAGE: ${MEMORY_USAGE}%"
            log_message "$ALERT"
            echo "[$(date '+%Y-%m-%d %H:%M:%S')] $ALERT" >> "$ALERT_FILE"
        fi
    fi
}

# Function to monitor system
monitor_system() {
    log_message "Starting automated system monitoring..."
    
    while true; do
        check_cpu_load
        check_memory_usage
        
        # Wait for next check
        sleep 30
    done
}

# Signal handler for graceful shutdown
cleanup() {
    log_message "Monitoring stopped by user"
    exit 0
}

trap cleanup SIGINT SIGTERM

# Start monitoring
echo "Starting automated performance monitoring..."
echo "Log file: $LOG_FILE"
echo "Alert file: $ALERT_FILE"
echo "Press Ctrl+C to stop monitoring"
echo

monitor_system
EOF

chmod +x automated_monitor.sh
Subtask 3.4: Test All Scripts

Run and test all the created scripts:

# Test the performance collector
echo "Testing performance collector..."
./performance_collector.sh

# Test the performance analyzer
echo "Testing performance analyzer..."
./performance_analyzer.sh

# View the generated reports
echo "Viewing performance report..."
ls -la /tmp/pcp_reports/

# Display the latest performance report
LATEST_REPORT=$(ls -t /tmp/pcp_reports/performance_report_*.txt | head -1)
if [ -f "$LATEST_REPORT" ]; then
    echo "Latest Performance Report:"
    head -50 "$LATEST_REPORT"
fi

# Display the latest analysis report
LATEST_ANALYSIS=$(ls -t /tmp/pcp_reports/performance_analysis_*.txt | head -1)
if [ -f "$LATEST_ANALYSIS" ]; then
    echo "Latest Analysis Report:"
    cat "$LATEST_ANALYSIS"
fi
