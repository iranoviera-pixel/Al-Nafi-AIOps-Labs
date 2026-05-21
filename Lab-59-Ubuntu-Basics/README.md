Lab 59: Introduction to Open Source Antivirus

Objectives

By the end of this lab, you will be able to:

Install and configure ClamAV, an open-source antivirus solution.
Update antivirus definitions using freshclam.
Automate daily virus scans using a custom script.
Interpret scan results and handle output files.
Prerequisites

A Linux system (Ubuntu/Debian/CentOS) with sudo privileges.
Basic familiarity with Linux command line.
Internet access for downloading packages.
Task 1: Install ClamAV

Step 1.1: Install ClamAV

ClamAV is a widely used open-source antivirus for Linux. Install it using your distribution's package manager.

For Ubuntu/Debian:

sudo apt update
sudo apt install clamav clamav-daemon -y
For CentOS/RHEL:

sudo yum install epel-release -y
sudo yum install clamav clamav-update -y
Expected Outcome:

ClamAV and its daemon are installed. Verify with:

clamscan --version
Troubleshooting:

If clamscan is not found, ensure the package installed correctly and /usr/bin is in your PATH.
Step 1.2: Start and Enable ClamAV Daemon

Start the ClamAV daemon for real-time protection (optional but recommended).

sudo systemctl start clamav-daemon
sudo systemctl enable clamav-daemon
Verify Status:

sudo systemctl status clamav-daemon
Expected Outcome:

The service should be active (running).

Task 2: Update Antivirus Definitions with freshclam

Step 2.1: Update Definitions

ClamAV relies on up-to-date virus definitions. Update them manually first:

sudo freshclam
Expected Outcome:

Database updates are downloaded. Output resembles:

ClamAV update process started at [timestamp]
main.cvd is up to date...
Troubleshooting:

If freshclam fails, check internet connectivity or proxy settings in /etc/clamav/freshclam.conf.
Step 2.2: Configure Automatic Updates

Edit the freshclam configuration to auto-update:

sudo nano /etc/clamav/freshclam.conf
Uncomment or add:

Checks 24
DatabaseMirror database.clamav.net
Restart the service:

sudo systemctl restart clamav-freshclam
Expected Outcome:

Definitions update automatically every 24 hours.

Task 3: Automate Daily Scans with a Script

Step 3.1: Create a Scan Script

Write a bash script to scan a directory (e.g., /home) and log results.

#!/bin/bash
SCAN_DIR="/home"
LOG_FILE="/var/log/clamav/daily_scan.log"
EMAIL="admin@example.com"

# Ensure log directory exists
sudo mkdir -p /var/log/clamav
sudo touch $LOG_FILE

# Run scan
echo "Starting daily ClamAV scan at $(date)" >> $LOG_FILE
clamscan -r --infected --log=$LOG_FILE $SCAN_DIR

# Email results (requires mailutils/postfix)
if grep -q "Infected files: [1-9]" $LOG_FILE; then
    mail -s "ClamAV: Infected Files Detected" $EMAIL < $LOG_FILE
fi
Save as /usr/local/bin/daily_clamscan.sh and make it executable:

sudo chmod +x /usr/local/bin/daily_clamscan.sh
Key Concepts:

-r: Recursive scan.
--infected: Only report infected files.
grep: Checks if infections were found.
Step 3.2: Schedule the Script with Cron

Add a cron job to run the script daily at 2 AM.

sudo crontab -e
Add:

0 2 * * * /usr/local/bin/daily_clamscan.sh
Verify Cron Job:

sudo crontab -l
Expected Outcome:

The script runs daily, logging to /var/log/clamav/daily_scan.log.
