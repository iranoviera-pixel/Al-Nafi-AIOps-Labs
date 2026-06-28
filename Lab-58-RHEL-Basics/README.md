Lab 58: Automating System Monitoring with sar and cron

Objectives

By the end of this lab, students will be able to:

Configure sar (System Activity Reporter) to collect system performance metrics.
Schedule automated data collection using cron.
Generate and interpret system reports from collected sar data.
Prerequisites

Before starting, ensure you have:

A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with Linux command-line operations.
Administrative (sudo) privileges to install packages and modify system configurations.
Task 1: Configure sar to Collect System Metrics

Step 1: Install sysstat Package

sar is part of the sysstat package. Install it using:

sudo apt update && sudo apt install sysstat -y
Expected Outcome:
The sysstat package is installed, enabling sar and related tools.

Step 2: Enable sar Data Collection

By default, sar may not be active. Edit its configuration:

sudo nano /etc/default/sysstat
Change the following line to enable data collection:

ENABLED="true"
Restart the service:

sudo systemctl restart sysstat
Expected Outcome:
sar begins collecting system metrics every 10 minutes (default interval).

Step 3: Verify sar Data Collection

Check if data is being logged:

sar -u 1 3  # CPU usage, 1-second intervals, 3 times
Troubleshooting:
If no data appears, ensure the service is running:

sudo systemctl status sysstat
Task 2: Schedule sar Reports Using cron

Step 1: Create a Script to Generate Reports

Write a script (/home/user/sar_report.sh) to save sar output daily:

#!/bin/bash
DATE=$(date +%Y-%m-%d)
sar -A > "/home/user/sar_report_$DATE.log"  # -A: All metrics
Make it executable:

chmod +x /home/user/sar_report.sh
Step 2: Schedule the Script with cron

Edit the crontab file:

crontab -e
Add this line to run the script daily at 11:59 PM:

59 23 * * * /home/user/sar_report.sh
Expected Outcome:
A new report (sar_report_YYYY-MM-DD.log) is generated daily in /home/user/.

Task 3: Automate Performance Reports

Step 1: Extract Key Metrics

Modify the script to extract CPU and memory usage:

#!/bin/bash
DATE=$(date +%Y-%m-%d)
echo "CPU Usage:" > "/home/user/sar_summary_$DATE.log"
sar -u >> "/home/user/sar_summary_$DATE.log"
echo -e "\nMemory Usage:" >> "/home/user/sar_summary_$DATE.log"
sar -r >> "/home/user/sar_summary_$DATE.log"
Step 2: Email Reports (Optional)

Install mailutils to email reports:

sudo apt install mailutils -y
Add this to the script (replace user@example.com):

mail -s "System Report $DATE" user@example.com < "/home/user/sar_summary_$DATE.log"
Expected Outcome:
A summarized report is generated and optionally emailed daily.
