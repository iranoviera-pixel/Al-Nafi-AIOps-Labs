Lab 51: Journald and Log Management

Objectives

By the end of this lab, students will be able to:

Understand the fundamentals of systemd journald logging service
Configure journald settings for effective log management
Use journalctl command to view, filter, and analyze system logs
Create automated scripts for log rotation and management
Implement best practices for system log monitoring and maintenance
Prerequisites

Before starting this lab, students should have:

Basic understanding of Linux command line interface
Familiarity with text editors (nano, vim, or gedit)
Knowledge of basic shell scripting concepts
Understanding of file permissions and system directories
Basic knowledge of systemd services
Lab Environment Setup

Ready-to-Use Cloud Machines: Al Nafi provides pre-configured Linux-based cloud machines for this lab. Simply click Start Lab to access your environment - no need to build your own virtual machine or install additional software.

Your lab environment includes:

Ubuntu 20.04 LTS or CentOS 8 with systemd
Pre-installed journald service
Root and sudo access
All necessary tools and utilities
Task 1: Configure Journald for Log Management

Subtask 1.1: Understanding Journald Configuration

First, let's explore the current journald configuration and understand its structure.

Step 1: Check if journald service is running

sudo systemctl status systemd-journald
Step 2: Locate and examine the main journald configuration file

sudo cat /etc/systemd/journald.conf
Step 3: Create a backup of the original configuration

sudo cp /etc/systemd/journald.conf /etc/systemd/journald.conf.backup
Subtask 1.2: Configuring Storage Settings

Step 1: Open the journald configuration file for editing

sudo nano /etc/systemd/journald.conf
Step 2: Configure storage settings by modifying these parameters

[Journal]
Storage=persistent
Compress=yes
SystemMaxUse=500M
SystemKeepFree=1G
SystemMaxFileSize=50M
SystemMaxFiles=10
MaxRetentionSec=1month
Key Configuration Parameters Explained:

Storage=persistent: Stores logs on disk permanently
Compress=yes: Compresses log files to save space
SystemMaxUse=500M: Maximum disk space for all journal files
SystemKeepFree=1G: Minimum free space to maintain on disk
SystemMaxFileSize=50M: Maximum size for individual journal files
SystemMaxFiles=10: Maximum number of journal files to keep
MaxRetentionSec=1month: Keep logs for one month
Step 3: Save the file and restart journald service

sudo systemctl restart systemd-journald
Step 4: Verify the configuration changes

sudo systemctl status systemd-journald
journalctl --disk-usage
Subtask 1.3: Setting Up Log Forwarding

Step 1: Configure journald to forward logs to syslog (optional)

sudo nano /etc/systemd/journald.conf
Step 2: Add or modify the ForwardToSyslog setting

ForwardToSyslog=yes
ForwardToKMsg=no
ForwardToConsole=no
Step 3: Restart the service to apply changes

sudo systemctl restart systemd-journald
Task 2: Use Journalctl to View and Filter Logs

Subtask 2.1: Basic Log Viewing Commands

Step 1: View all journal entries

journalctl
Step 2: View logs in real-time (similar to tail -f)

journalctl -f
Step 3: View logs from the current boot

journalctl -b
Step 4: View logs from previous boots

journalctl --list-boots
journalctl -b -1
Subtask 2.2: Filtering Logs by Time and Priority

Step 1: View logs from the last hour

journalctl --since "1 hour ago"
Step 2: View logs from a specific date range

journalctl --since "2024-01-01" --until "2024-01-02"
Step 3: View logs by priority level

# View only error messages
journalctl -p err

# View warning and above
journalctl -p warning

# View info and above
journalctl -p info
Step 4: Combine time and priority filters

journalctl --since "1 hour ago" -p err
Subtask 2.3: Filtering by Service and Unit

Step 1: View logs for a specific service

journalctl -u ssh
journalctl -u apache2
journalctl -u nginx
Step 2: View logs for multiple services

journalctl -u ssh -u apache2
Step 3: View logs for a specific process ID

journalctl _PID=1234
Step 4: View kernel messages

journalctl -k
Subtask 2.4: Advanced Filtering and Output Formatting

Step 1: Create a script to demonstrate advanced filtering

nano advanced_log_filter.sh
Step 2: Add the following content to the script

#!/bin/bash

echo "=== Advanced Journalctl Filtering Demo ==="
echo

echo "1. Logs from specific user:"
journalctl _UID=1000 --since "today" | head -10

echo
echo "2. Logs with specific message pattern:"
journalctl --grep="error" --since "1 hour ago" | head -5

echo
echo "3. JSON formatted output:"
journalctl -u ssh -o json --lines=3

echo
echo "4. Logs from specific executable:"
journalctl /usr/sbin/sshd --since "today" | head -5

echo
echo "5. Disk usage information:"
journalctl --disk-usage

echo
echo "6. Available boots:"
journalctl --list-boots
Step 3: Make the script executable and run it

chmod +x advanced_log_filter.sh
./advanced_log_filter.sh
Task 3: Write a Script to Automate Log Rotation and Management

Subtask 3.1: Creating a Log Management Script

Step 1: Create a comprehensive log management script

nano log_management_script.sh
Step 2: Add the following content to create a full-featured log management script

#!/bin/bash

# Log Management Script for Journald
# Author: System Administrator
# Purpose: Automate log rotation, cleanup, and monitoring

# Configuration variables
LOG_FILE="/var/log/log_management.log"
MAX_DISK_USAGE="400M"
RETENTION_DAYS=30
EMAIL_ALERT="admin@example.com"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | sudo tee -a "$LOG_FILE"
}

# Function to check disk usage
check_disk_usage() {
    log_message "Checking journal disk usage..."
    
    CURRENT_USAGE=$(journalctl --disk-usage | grep -oP '\d+\.\d+[MG]' | head -1)
    log_message "Current journal disk usage: $CURRENT_USAGE"
    
    # Convert to bytes for comparison (simplified)
    USAGE_BYTES=$(journalctl --disk-usage | grep -oP '\d+' | head -1)
    MAX_BYTES=419430400  # 400MB in bytes
    
    if [ "$USAGE_BYTES" -gt "$MAX_BYTES" ]; then
        log_message "WARNING: Journal disk usage exceeds threshold!"
        return 1
    else
        log_message "Journal disk usage is within acceptable limits."
        return 0
    fi
}

# Function to clean old logs
clean_old_logs() {
    log_message "Starting log cleanup process..."
    
    # Clean logs older than retention period
    sudo journalctl --vacuum-time=${RETENTION_DAYS}d
    log_message "Cleaned logs older than $RETENTION_DAYS days"
    
    # Clean logs exceeding size limit
    sudo journalctl --vacuum-size="$MAX_DISK_USAGE"
    log_message "Cleaned logs exceeding $MAX_DISK_USAGE"
    
    # Clean logs exceeding file count
    sudo journalctl --vacuum-files=10
    log_message "Maintained maximum of 10 log files"
}

# Function to rotate logs manually
rotate_logs() {
    log_message "Initiating manual log rotation..."
    
    # Force log rotation
    sudo systemctl kill --kill-who=main --signal=SIGUSR2 systemd-journald
    log_message "Log rotation signal sent to journald"
    
    sleep 2
    
    # Verify rotation
    sudo systemctl status systemd-journald --no-pager
    log_message "Log rotation completed"
}

# Function to generate log report
generate_report() {
    log_message "Generating log management report..."
    
    REPORT_FILE="/tmp/journal_report_$(date +%Y%m%d_%H%M%S).txt"
    
    {
        echo "=== Journal Log Management Report ==="
        echo "Generated on: $(date)"
        echo
        echo "=== Disk Usage ==="
        journalctl --disk-usage
        echo
        echo "=== Available Boots ==="
        journalctl --list-boots
        echo
        echo "=== Recent Error Messages ==="
        journalctl -p err --since "24 hours ago" --lines=10
        echo
        echo "=== Service Status ==="
        systemctl status systemd-journald --no-pager
        echo
        echo "=== Configuration Summary ==="
        grep -v '^#' /etc/systemd/journald.conf | grep -v '^$'
    } > "$REPORT_FILE"
    
    log_message "Report generated: $REPORT_FILE"
    echo "Report saved to: $REPORT_FILE"
}

# Function to monitor critical services
monitor_services() {
    log_message "Monitoring critical services..."
    
    SERVICES=("ssh" "systemd-journald" "cron")
    
    for service in "${SERVICES[@]}"; do
        if systemctl is-active --quiet "$service"; then
            log_message "Service $service is running normally"
        else
            log_message "ALERT: Service $service is not running!"
            # In a real environment, you might send an email alert here
        fi
    done
}

# Function to backup journal configuration
backup_config() {
    log_message "Backing up journal configuration..."
    
    BACKUP_DIR="/var/backups/journald"
    sudo mkdir -p "$BACKUP_DIR"
    
    sudo cp /etc/systemd/journald.conf "$BACKUP_DIR/journald.conf.$(date +%Y%m%d_%H%M%S)"
    log_message "Configuration backed up to $BACKUP_DIR"
}

# Main execution function
main() {
    log_message "=== Starting Log Management Script ==="
    
    case "$1" in
        "check")
            check_disk_usage
            ;;
        "clean")
            clean_old_logs
            ;;
        "rotate")
            rotate_logs
            ;;
        "report")
            generate_report
            ;;
        "monitor")
            monitor_services
            ;;
        "backup")
            backup_config
            ;;
        "full")
            backup_config
            check_disk_usage
            if [ $? -eq 1 ]; then
                clean_old_logs
            fi
            monitor_services
            generate_report
            ;;
        *)
            echo "Usage: $0 {check|clean|rotate|report|monitor|backup|full}"
            echo
            echo "Commands:"
            echo "  check   - Check current disk usage"
            echo "  clean   - Clean old logs based on retention policy"
            echo "  rotate  - Force log rotation"
            echo "  report  - Generate comprehensive log report"
            echo "  monitor - Monitor critical services"
            echo "  backup  - Backup journal configuration"
            echo "  full    - Run complete maintenance routine"
            exit 1
            ;;
    esac
    
    log_message "=== Log Management Script Completed ==="
}

# Execute main function with provided argument
main "$1"
Step 3: Make the script executable

chmod +x log_management_script.sh
Subtask 3.2: Testing the Log Management Script

Step 1: Test individual script functions

# Check disk usage
./log_management_script.sh check

# Generate a report
./log_management_script.sh report

# Monitor services
./log_management_script.sh monitor
Step 2: Run the full maintenance routine

./log_management_script.sh full
Step 3: View the generated report

ls -la /tmp/journal_report_*
cat /tmp/journal_report_*.txt
Subtask 3.3: Setting Up Automated Execution

Step 1: Create a cron job for automated log management

sudo crontab -e
Step 2: Add the following cron entries

# Run full log management daily at 2 AM
0 2 * * * /path/to/log_management_script.sh full

# Check disk usage every 6 hours
0 */6 * * * /path/to/log_management_script.sh check

# Generate weekly reports on Sundays at 6 AM
0 6 * * 0 /path/to/log_management_script.sh report
Step 3: Create a systemd timer as an alternative to cron

sudo nano /etc/systemd/system/log-management.service
Step 4: Add the service definition

[Unit]
Description=Journal Log Management Service
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/path/to/log_management_script.sh full
User=root
Step 5: Create the timer file

sudo nano /etc/systemd/system/log-management.timer
Step 6: Add the timer configuration

[Unit]
Description=Run log management daily
Requires=log-management.service

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
Step 7: Enable and start the timer

sudo systemctl daemon-reload
sudo systemctl enable log-management.timer
sudo systemctl start log-management.timer
sudo systemctl status log-management.timer
