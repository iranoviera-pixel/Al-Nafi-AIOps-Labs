Lab 57: Automating Log Management with Journald

Objectives

By the end of this lab, students will be able to:

Understand the basics of journald and log management in Linux.
Automate log rotation based on time or size.
Implement log compression and removal using retention policies.
Export logs from journald to a file for archival purposes.
Prerequisites

Before starting this lab, students should have:

Basic familiarity with Linux command line.
Access to a Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Understanding of fundamental concepts like files, directories, and permissions.
Lab Setup

Note: If using Al Nafi's cloud machine, skip setup steps—your environment is ready.

Verify SystemD and Journald:
Run the following command to check if journald is active:

systemctl status systemd-journald
Expected Output:
Active status should show "active (running)".

Install Required Tools (if needed):
Most systems come with journalctl, but ensure compression tools are available:

sudo apt-get install gzip tar  # For Debian/Ubuntu
sudo yum install gzip tar      # For CentOS/RHEL
Task 1: Rotate Logs Based on Time or Size

Step 1: Configure Journald for Log Rotation

Open the journald configuration file:
sudo nano /etc/systemd/journald.conf
Uncomment/modify the following lines to set size-based rotation (e.g., 100MB):
SystemMaxUse=100M
RuntimeMaxUse=100M
For time-based rotation, add:
MaxFileSec=1day
Restart journald to apply changes:
sudo systemctl restart systemd-journald
Expected Outcome:
Logs will rotate automatically when they exceed 100MB or after 1 day.

Task 2: Automate Log Compression and Retention

Step 1: Create a Log Cleanup Script

Create a script named rotate_journald_logs.sh:
sudo nano /usr/local/bin/rotate_journald_logs.sh
Paste the following script to compress logs older than 7 days and delete those older than 30 days:
#!/bin/bash
# Compress logs older than 7 days
journalctl --vacuum-time=7d --quiet
# Remove archived logs older than 30 days
find /var/log/journal -name "*.journal" -mtime +30 -exec rm {} \;
Make the script executable:
sudo chmod +x /usr/local/bin/rotate_journald_logs.sh
Step 2: Schedule the Script with Cron

Open the cron table:
sudo crontab -e
Add this line to run the script daily at midnight:
0 0 * * * /usr/local/bin/rotate_journald_logs.sh
Expected Outcome:
Logs older than 7 days will be compressed, and logs older than 30 days will be deleted automatically.

Task 3: Export Logs to a File for Archival

Step 1: Export Logs to a File

Use journalctl to export logs from the last 24 hours to a file:
journalctl --since "24 hours ago" > /var/log/journal_export_$(date +%Y-%m-%d).log
Compress the exported log:
gzip /var/log/journal_export_$(date +%Y-%m-%d).log
Expected Outcome:
A compressed log file (e.g., journal_export_2023-10-01.log.gz) will be created in /var/log/.

Troubleshooting Tips

Permission Denied:
Use sudo for commands accessing /var/log/ or system files.
Journald Not Restarting:
Run sudo systemctl daemon-reload before restarting journald.
Cron Job Failing:
Check logs with sudo tail -f /var/log/syslog for errors.
