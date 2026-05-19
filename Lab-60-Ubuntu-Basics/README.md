Lab 60: Introduction to rkhunter

Objectives

By the end of this lab, you will be able to:

Install and configure rkhunter (Rootkit Hunter) on a Linux system.
Perform manual and automated scans for rootkits and suspicious activities.
Write a Bash script to automate rkhunter scans and email alerts.
Prerequisites

A Linux system (Ubuntu/Debian/CentOS)
Sudo or root privileges
Basic familiarity with Linux command line
mailutils or postfix installed for email alerts (optional)
Task 1: Install and Configure rkhunter

Subtask 1.1: Install rkhunter

Update your package list:

sudo apt update  # Debian/Ubuntu
sudo yum update  # CentOS/RHEL
Install rkhunter:

sudo apt install rkhunter -y  # Debian/Ubuntu
sudo yum install rkhunter -y  # CentOS/RHEL
Expected Outcome:
rkhunter is installed without errors. Verify with:

rkhunter --version
Subtask 1.2: Configure rkhunter

Update the file properties database:

sudo rkhunter --propupd
Edit the configuration file to customize settings (e.g., email alerts):

sudo nano /etc/rkhunter.conf
Uncomment/modify these lines:
MAIL-ON-WARNING=your-email@example.com
REPORT_EMAIL=your-email@example.com
Troubleshooting Tip:
If mailutils is not installed, run sudo apt install mailutils (Debian/Ubuntu) or sudo yum install mailx (CentOS).

Task 2: Perform a Rootkit Scan

Subtask 2.1: Run a Manual Scan

Execute a basic scan:

sudo rkhunter --check
Review the log file for results:

sudo cat /var/log/rkhunter.log
Expected Outcome:
A summary of checks with warnings/errors (if any). Example:

[ OK ]  No known rootkits detected.
[ WARNING ]  Suspicious file permissions found.
Subtask 2.2: Update and Verify Signatures

Update rkhunter definitions:

sudo rkhunter --update
Verify system commands:

sudo rkhunter --check --sk
Task 3: Automate Scans with Email Alerts

Subtask 3.1: Create a Bash Script

Create a script file:

nano rkhunter_scan.sh
Paste the following (replace your-email@example.com):

#!/bin/bash
LOG_FILE="/var/log/rkhunter.log"
EMAIL="your-email@example.com"

echo "Starting rkhunter scan..."
sudo rkhunter --check --sk --rwo > "$LOG_FILE"

if grep -q "Warning" "$LOG_FILE"; then
    echo "Sending alert email..."
    mail -s "rkhunter ALERT: Suspicious Activity Detected" "$EMAIL" < "$LOG_FILE"
else
    echo "No threats detected."
fi
Make the script executable:

chmod +x rkhunter_scan.sh
Subtask 3.2: Schedule with Cron

Open the cron table:

crontab -e
Add a daily scan (runs at 2 AM):

0 2 * * * /path/to/rkhunter_scan.sh
Expected Outcome:
The script runs daily, and emails are sent if warnings are detected.


