Lab 9: Automating File Backup with Scripts

Lab Objectives

By the end of this lab, students will be able to:

Create a Bash script that automatically backs up files and directories
Schedule automated backups using the cron job scheduler
Implement backup verification and error notification systems
Understand the importance of automated backup strategies
Apply basic shell scripting concepts for system administration tasks
Prerequisites

Before starting this lab, students should have:

Basic understanding of Linux command line operations
Familiarity with file and directory navigation in Linux
Basic knowledge of text editors (nano, vim, or gedit)
Understanding of file permissions in Linux
No prior scripting experience required - we'll guide you through everything
Lab Environment Setup

Ready-to-Use Cloud Machines: Al Nafi provides pre-configured Linux-based cloud machines for this lab. Simply click Start Lab to access your environment - no need to build or configure your own virtual machine. Your lab environment includes all necessary tools and permissions to complete the exercises.

Task 1: Creating a Basic File Backup Script

Subtask 1.1: Setting Up the Lab Directory Structure

First, let's create a proper directory structure for our backup lab:

# Create main lab directory
mkdir -p ~/backup-lab

# Navigate to the lab directory
cd ~/backup-lab

# Create directories for our work
mkdir -p source-files backup-destination scripts logs

# Create some sample files to backup
echo "This is document 1" > source-files/document1.txt
echo "This is document 2" > source-files/document2.txt
echo "Important data file" > source-files/important-data.txt

# Create a subdirectory with more files
mkdir -p source-files/projects
echo "Project A content" > source-files/projects/project-a.txt
echo "Project B content" > source-files/projects/project-b.txt

# Verify our structure
ls -la source-files/
ls -la source-files/projects/
Subtask 1.2: Writing the Basic Backup Script

Now let's create our first backup script. This script will copy files from a source directory to a backup destination:

# Navigate to the scripts directory
cd ~/backup-lab/scripts

# Create the backup script using nano editor
nano basic-backup.sh
Copy and paste the following script into the nano editor:

#!/bin/bash

# Basic File Backup Script
# This script backs up files from a source directory to a backup destination

# Define variables
SOURCE_DIR="$HOME/backup-lab/source-files"
BACKUP_DIR="$HOME/backup-lab/backup-destination"
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_NAME="backup_$DATE"
LOG_FILE="$HOME/backup-lab/logs/backup.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Start backup process
log_message "Starting backup process..."

# Check if source directory exists
if [ ! -d "$SOURCE_DIR" ]; then
    log_message "ERROR: Source directory $SOURCE_DIR does not exist!"
    exit 1
fi

# Create backup directory if it doesn't exist
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    log_message "Created backup directory: $BACKUP_DIR"
fi

# Create timestamped backup folder
FULL_BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"
mkdir -p "$FULL_BACKUP_PATH"

# Copy files to backup location
log_message "Copying files from $SOURCE_DIR to $FULL_BACKUP_PATH"

if cp -r "$SOURCE_DIR"/* "$FULL_BACKUP_PATH"/; then
    log_message "Backup completed successfully!"
    log_message "Backup location: $FULL_BACKUP_PATH"
    
    # Count files backed up
    FILE_COUNT=$(find "$FULL_BACKUP_PATH" -type f | wc -l)
    log_message "Total files backed up: $FILE_COUNT"
else
    log_message "ERROR: Backup failed!"
    exit 1
fi

log_message "Backup process finished."
Save the file by pressing Ctrl+X, then Y, then Enter.

Subtask 1.3: Making the Script Executable and Testing

# Make the script executable
chmod +x basic-backup.sh

# Test the script
./basic-backup.sh

# Check if backup was created
ls -la ~/backup-lab/backup-destination/

# View the log file
cat ~/backup-lab/logs/backup.log
Subtask 1.4: Verifying the Backup

Let's verify that our backup worked correctly:

# Compare source and backup directories
echo "Source directory contents:"
find ~/backup-lab/source-files -type f

echo -e "\nBackup directory contents:"
find ~/backup-lab/backup-destination -name "*.txt"

# Check file contents to ensure they match
echo -e "\nVerifying file contents:"
diff ~/backup-lab/source-files/document1.txt ~/backup-lab/backup-destination/backup_*/document1.txt
Task 2: Scheduling the Backup Script with Cron

Subtask 2.1: Understanding Cron Syntax

Before we schedule our backup, let's understand cron syntax:

* * * * * command
│ │ │ │ │
│ │ │ │ └─── Day of week (0-7, Sunday = 0 or 7)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
Common Examples:

0 2 * * * - Run daily at 2:00 AM
30 14 * * 1 - Run every Monday at 2:30 PM
0 */6 * * * - Run every 6 hours
*/15 * * * * - Run every 15 minutes
Subtask 2.2: Creating an Enhanced Backup Script for Cron

Let's create an improved version of our backup script that's better suited for cron scheduling:

# Create enhanced backup script
cd ~/backup-lab/scripts
nano daily-backup.sh
Copy the following enhanced script:

#!/bin/bash

# Enhanced Daily Backup Script for Cron
# This script includes better error handling and cleanup features

# Configuration variables
SOURCE_DIR="$HOME/backup-lab/source-files"
BACKUP_DIR="$HOME/backup-lab/backup-destination"
LOG_FILE="$HOME/backup-lab/logs/daily-backup.log"
MAX_BACKUPS=7  # Keep only 7 days of backups
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_NAME="daily_backup_$DATE"

# Function to log messages with timestamps
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to send notification (for demonstration)
send_notification() {
    local message="$1"
    log_message "NOTIFICATION: $message"
    # In a real environment, you might send email or use other notification methods
    echo "$message" >> "$HOME/backup-lab/logs/notifications.log"
}

# Start backup process
log_message "=== Starting daily backup process ==="

# Validate source directory
if [ ! -d "$SOURCE_DIR" ]; then
    send_notification "ERROR: Source directory $SOURCE_DIR not found!"
    exit 1
fi

# Create backup directory structure
mkdir -p "$BACKUP_DIR"
mkdir -p "$(dirname "$LOG_FILE")"

# Create timestamped backup folder
FULL_BACKUP_PATH="$BACKUP_DIR/$BACKUP_NAME"
mkdir -p "$FULL_BACKUP_PATH"

# Perform backup with error checking
log_message "Backing up from $SOURCE_DIR to $FULL_BACKUP_PATH"

if cp -r "$SOURCE_DIR"/* "$FULL_BACKUP_PATH"/ 2>/dev/null; then
    # Count backed up files
    FILE_COUNT=$(find "$FULL_BACKUP_PATH" -type f | wc -l)
    BACKUP_SIZE=$(du -sh "$FULL_BACKUP_PATH" | cut -f1)
    
    log_message "Backup completed successfully!"
    log_message "Files backed up: $FILE_COUNT"
    log_message "Backup size: $BACKUP_SIZE"
    log_message "Backup location: $FULL_BACKUP_PATH"
    
    send_notification "Daily backup completed successfully - $FILE_COUNT files backed up"
else
    send_notification "ERROR: Backup operation failed!"
    exit 1
fi

# Cleanup old backups (keep only MAX_BACKUPS)
log_message "Cleaning up old backups (keeping $MAX_BACKUPS most recent)"

cd "$BACKUP_DIR"
BACKUP_COUNT=$(ls -1 | grep "daily_backup_" | wc -l)

if [ "$BACKUP_COUNT" -gt "$MAX_BACKUPS" ]; then
    BACKUPS_TO_DELETE=$((BACKUP_COUNT - MAX_BACKUPS))
    ls -1t | grep "daily_backup_" | tail -n "$BACKUPS_TO_DELETE" | while read backup; do
        log_message "Removing old backup: $backup"
        rm -rf "$backup"
    done
    log_message "Cleanup completed - removed $BACKUPS_TO_DELETE old backups"
fi

log_message "=== Daily backup process completed ==="
Save and make executable:

# Save the file (Ctrl+X, Y, Enter)
chmod +x daily-backup.sh

# Test the enhanced script
./daily-backup.sh

# Check the results
cat ~/backup-lab/logs/daily-backup.log
Subtask 2.3: Setting Up Cron Job

Now let's schedule our backup script to run daily:

# Open crontab for editing
crontab -e
If prompted to choose an editor, select nano (usually option 1).

Add the following line to schedule daily backup at 2:00 AM:

# Daily backup at 2:00 AM
0 2 * * * /home/$USER/backup-lab/scripts/daily-backup.sh
For testing purposes, let's also add a job that runs every 5 minutes:

# Test backup every 5 minutes (remove this after testing)
*/5 * * * * /home/$USER/backup-lab/scripts/daily-backup.sh
Save and exit (Ctrl+X, Y, Enter).

Subtask 2.4: Verifying Cron Configuration

# List current cron jobs
crontab -l

# Check if cron service is running
systemctl status cron

# Monitor the log file to see if cron jobs are running
tail -f ~/backup-lab/logs/daily-backup.log
Wait for 5 minutes to see if the test cron job executes, then remove the test job:

# Edit crontab to remove the test job
crontab -e
# Remove the line with */5 * * * *
Task 3: Creating Backup Verification and Notification Script

Subtask 3.1: Writing a Backup Verification Script

Let's create a script that verifies backup integrity and sends notifications:

cd ~/backup-lab/scripts
nano backup-verify.sh
Copy the following verification script:

#!/bin/bash

# Backup Verification and Notification Script
# This script checks backup integrity and sends notifications

# Configuration
SOURCE_DIR="$HOME/backup-lab/source-files"
BACKUP_DIR="$HOME/backup-lab/backup-destination"
LOG_FILE="$HOME/backup-lab/logs/verification.log"
NOTIFICATION_LOG="$HOME/backup-lab/logs/notifications.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Function to send notification
send_notification() {
    local status="$1"
    local message="$2"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    echo "[$timestamp] $status: $message" >> "$NOTIFICATION_LOG"
    log_message "NOTIFICATION SENT: $status - $message"
    
    # In a production environment, you might send emails or use other notification services
    # For demonstration, we'll just log to file and display
    echo "🔔 NOTIFICATION: $status - $message"
}

# Function to verify backup integrity
verify_backup() {
    local backup_path="$1"
    local errors=0
    
    log_message "Verifying backup: $backup_path"
    
    # Check if backup directory exists
    if [ ! -d "$backup_path" ]; then
        log_message "ERROR: Backup directory not found: $backup_path"
        return 1
    fi
    
    # Count files in source and backup
    local source_files=$(find "$SOURCE_DIR" -type f | wc -l)
    local backup_files=$(find "$backup_path" -type f | wc -l)
    
    log_message "Source files: $source_files, Backup files: $backup_files"
    
    if [ "$source_files" -ne "$backup_files" ]; then
        log_message "ERROR: File count mismatch!"
        ((errors++))
    fi
    
    # Verify file contents (sample check)
    while IFS= read -r -d '' source_file; do
        local relative_path="${source_file#$SOURCE_DIR/}"
        local backup_file="$backup_path/$relative_path"
        
        if [ ! -f "$backup_file" ]; then
            log_message "ERROR: Missing backup file: $relative_path"
            ((errors++))
        elif ! cmp -s "$source_file" "$backup_file"; then
            log_message "ERROR: Content mismatch: $relative_path"
            ((errors++))
        fi
    done < <(find "$SOURCE_DIR" -type f -print0)
    
    return $errors
}

# Main verification process
log_message "=== Starting backup verification ==="

# Find the most recent backup
LATEST_BACKUP=$(ls -1t "$BACKUP_DIR" | grep "daily_backup_" | head -n 1)

if [ -z "$LATEST_BACKUP" ]; then
    send_notification "ERROR" "No backup found in $BACKUP_DIR"
    exit 1
fi

LATEST_BACKUP_PATH="$BACKUP_DIR/$LATEST_BACKUP"
log_message "Checking latest backup: $LATEST_BACKUP"

# Verify the backup
if verify_backup "$LATEST_BACKUP_PATH"; then
    # Calculate backup age
    BACKUP_DATE=$(echo "$LATEST_BACKUP" | grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}_[0-9]\{2\}-[0-9]\{2\}-[0-9]\{2\}')
    BACKUP_TIMESTAMP=$(date -d "${BACKUP_DATE//_/ }" +%s 2>/dev/null || date +%s)
    CURRENT_TIMESTAMP=$(date +%s)
    BACKUP_AGE_HOURS=$(( (CURRENT_TIMESTAMP - BACKUP_TIMESTAMP) / 3600 ))
    
    # Check if backup is recent (less than 25 hours old)
    if [ "$BACKUP_AGE_HOURS" -lt 25 ]; then
        send_notification "SUCCESS" "Backup verification passed. Backup is $BACKUP_AGE_HOURS hours old."
    else
        send_notification "WARNING" "Backup verification passed but backup is $BACKUP_AGE_HOURS hours old."
    fi
else
    send_notification "ERROR" "Backup verification failed! Please check the logs."
fi

log_message "=== Backup verification completed ==="
Save and make executable:

chmod +x backup-verify.sh

# Test the verification script
./backup-verify.sh

# Check the results
cat ~/backup-lab/logs/verification.log
cat ~/backup-lab/logs/notifications.log
Subtask 3.2: Creating a Comprehensive Monitoring Script

Let's create a script that monitors the entire backup system:

nano backup-monitor.sh
Copy the following monitoring script:

#!/bin/bash

# Comprehensive Backup Monitoring Script
# This script provides a complete status report of the backup system

# Configuration
BACKUP_DIR="$HOME/backup-lab/backup-destination"
LOG_DIR="$HOME/backup-lab/logs"
REPORT_FILE="$LOG_DIR/backup-report.txt"

# Function to create status report
create_report() {
    local report_file="$1"
    
    echo "=== BACKUP SYSTEM STATUS REPORT ===" > "$report_file"
    echo "Generated: $(date)" >> "$report_file"
    echo "" >> "$report_file"
    
    # Backup directory status
    echo "📁 BACKUP DIRECTORY STATUS:" >> "$report_file"
    if [ -d "$BACKUP_DIR" ]; then
        echo "✅ Backup directory exists: $BACKUP_DIR" >> "$report_file"
        
        # List all backups
        echo "" >> "$report_file"
        echo "📋 AVAILABLE BACKUPS:" >> "$report_file"
        ls -la "$BACKUP_DIR" | grep "backup_" >> "$report_file"
        
        # Count backups
        BACKUP_COUNT=$(ls -1 "$BACKUP_DIR" | grep "backup_" | wc -l)
        echo "" >> "$report_file"
        echo "📊 Total backups: $BACKUP_COUNT" >> "$report_file"
        
        # Latest backup info
        LATEST_BACKUP=$(ls -1t "$BACKUP_DIR" | grep "backup_" | head -n 1)
        if [ -n "$LATEST_BACKUP" ]; then
            echo "🕐 Latest backup: $LATEST_BACKUP" >> "$report_file"
            
            # Backup size
            BACKUP_SIZE=$(du -sh "$BACKUP_DIR/$LATEST_BACKUP" | cut -f1)
            echo "💾 Latest backup size: $BACKUP_SIZE" >> "$report_file"
            
            # File count in latest backup
            FILE_COUNT=$(find "$BACKUP_DIR/$LATEST_BACKUP" -type f | wc -l)
            echo "📄 Files in latest backup: $FILE_COUNT" >> "$report_file"
        fi
    else
        echo "❌ Backup directory not found!" >> "$report_file"
    fi
    
    echo "" >> "$report_file"
    
    # Cron job status
    echo "⏰ SCHEDULED BACKUP STATUS:" >> "$report_file"
    if crontab -l 2>/dev/null | grep -q "daily-backup.sh"; then
        echo "✅ Backup cron job is configured" >> "$report_file"
        echo "📅 Cron schedule:" >> "$report_file"
        crontab -l | grep "daily-backup.sh" >> "$report_file"
    else
        echo "❌ No backup cron job found!" >> "$report_file"
    fi
    
    echo "" >> "$report_file"
    
    # Log file analysis
    echo "📝 LOG FILE ANALYSIS:" >> "$report_file"
    
    if [ -f "$LOG_DIR/daily-backup.log" ]; then
        echo "✅ Daily backup log exists" >> "$report_file"
        
        # Recent log entries
        echo "" >> "$report_file"
        echo "🔍 Recent backup log entries (last 10):" >> "$report_file"
        tail -n 10 "$LOG_DIR/daily-backup.log" >> "$report_file"
        
        # Count successful backups
        SUCCESS_COUNT=$(grep -c "completed successfully" "$LOG_DIR/daily-backup.log" 2>/dev/null || echo "0")
        ERROR_COUNT=$(grep -c "ERROR" "$LOG_DIR/daily-backup.log" 2>/dev/null || echo "0")
        
        echo "" >> "$report_file"
        echo "📈 Backup statistics:" >> "$report_file"
        echo "   ✅ Successful backups: $SUCCESS_COUNT" >> "$report_file"
        echo "   ❌ Failed backups: $ERROR_COUNT" >> "$report_file"
    else
        echo "❌ Daily backup log not found!" >> "$report_file"
    fi
    
    echo "" >> "$report_file"
    
    # Disk space analysis
    echo "💽 DISK SPACE ANALYSIS:" >> "$report_file"
    echo "Backup directory disk usage:" >> "$report_file"
    du -sh "$BACKUP_DIR" 2>/dev/null >> "$report_file" || echo "Unable to calculate disk usage" >> "$report_file"
    
    echo "" >> "$report_file"
    echo "Available disk space:" >> "$report_file"
    df -h "$HOME" | tail -n 1 >> "$report_file"
    
    echo "" >> "$report_file"
    echo "=== END OF REPORT ===" >> "$report_file"
}

# Function to display colored output
display_report() {
    local report_file="$1"
    
    # Display report with colors (if terminal supports it)
    if [ -t 1 ]; then
        # Terminal output with colors
        sed 's/✅/\x1b[32m✅\x1b[0m/g; s/❌/\x1b[31m❌\x1b[0m/g; s/⚠️/\x1b[33m⚠️\x1b[0m/g' "$report_file"
    else
        # Plain output for non-terminal
        cat "$report_file"
    fi
}

# Main execution
echo "🔍 Generating backup system status report..."

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Generate report
create_report "$REPORT_FILE"

# Display report
display_report "$REPORT_FILE"

echo ""
echo "📄 Full report saved to: $REPORT_FILE"
Save and make executable:

chmod +x backup-monitor.sh

# Run the monitoring script
./backup-monitor.sh
Subtask 3.3: Setting Up Automated Monitoring

Let's schedule the monitoring script to run daily and send notifications:

# Edit crontab to add monitoring
crontab -e
Add the following lines:

# Daily backup at 2:00 AM
0 2 * * * /home/$USER/backup-lab/scripts/daily-backup.sh

# Backup verification at 3:00 AM (after backup completes)
0 3 * * * /home/$USER/backup-lab/scripts/backup-verify.sh

# Weekly backup system report every Sunday at 8:00 AM
0 8 * * 0 /home/$USER/backup-lab/scripts/backup-monitor.sh
Subtask 3.4: Testing the Complete System

Let's test our complete backup system:

# Run a complete test cycle
echo "🧪 Testing complete backup system..."

# 1. Run backup
echo "1. Running backup..."
~/backup-lab/scripts/daily-backup.sh

# 2. Verify backup
echo "2. Verifying backup..."
~/backup-lab/scripts/backup-verify.sh

# 3. Generate system report
echo "3. Generating system report..."
~/backup-lab/scripts/backup-monitor.sh

# 4. Check all log files
echo "4. Checking log files..."
echo "=== Backup Log ==="
tail -n 5 ~/backup-lab/logs/daily-backup.log

echo -e "\n=== Verification Log ==="
tail -n 5 ~/backup-lab/logs/verification.log

echo -e "\n=== Notifications ==="
tail -n 5 ~/backup-lab/logs/notifications.log
Troubleshooting Common Issues

Issue 1: Permission Denied Errors

# If you get permission denied errors, check file permissions
ls -la ~/backup-lab/scripts/

# Make sure all scripts are executable
chmod +x ~/backup-lab/scripts/*.sh
Issue 2: Cron Jobs Not Running

# Check if cron service is running
systemctl status cron

# Check cron logs
sudo tail -f /var/log/cron

# Verify crontab entries
crontab -l
Issue 3: Backup Directory Issues

# Check if directories exist and have proper permissions
ls -la ~/backup-lab/
mkdir -p ~/backup-lab/{source-files,backup-destination,scripts,logs}
Issue 4: Script Path Issues in Cron

# Use full paths in crontab entries
# Instead of: daily-backup.sh
# Use: /home/$USER/backup-lab/scripts/daily-backup.sh

# Check your home directory path
echo $HOME
Advanced Enhancements (Optional)

Email Notifications

If you want to add email notifications, you can install and configure mailutils:

# Install mail utilities (if not already installed)
sudo apt update
sudo apt install mailutils -y

# Add email notification to your scripts
send_email_notification() {
    local subject="$1"
    local message="$2"
    echo "$message" | mail -s "$subject" your-email@example.com
}
Compression and Encryption

Add compression and basic encryption to your backups:

# Add to your backup script
# Compress backup
tar -czf "$BACKUP_DIR/backup_$DATE.tar.gz" -C "$SOURCE_DIR" .

# Basic encryption (requires gpg setup)
gpg --symmetric --cipher-algo AES256 "$BACKUP_DIR/backup_$DATE.tar.gz"
