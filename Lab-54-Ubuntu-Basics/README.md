Lab 54: Scheduling Tasks with Cron

Objectives

By the end of this lab, you will be able to:

Understand the purpose and syntax of cron jobs.
Use crontab to schedule periodic tasks.
Create and manage cron jobs for system maintenance (e.g., log cleanup).
Write a shell script to automate daily tasks.
Prerequisites

A Linux-based system (Ubuntu/CentOS recommended).
Basic familiarity with the command line.
Root or sudo privileges for system-level tasks.
Task 1: Introduction to Cron and Crontab

Subtask 1.1: What is Cron?

Cron is a time-based job scheduler in Unix-like operating systems. It enables users to schedule jobs (commands or scripts) to run periodically at fixed times, dates, or intervals.

Subtask 1.2: Understanding Crontab Syntax

Cron jobs are defined in crontab files. The syntax for a cron job is:

* * * * * command-to-execute
┬ ┬ ┬ ┬ ┬
│ │ │ │ └── Day of week (0 - 6) (Sunday=0 or 7)
│ │ │ └──── Month (1 - 12)
│ │ └────── Day of month (1 - 31)
│ └──────── Hour (0 - 23)
└────────── Minute (0 - 59)
Subtask 1.3: Listing Existing Cron Jobs

Run the following command to view your user's cron jobs:

crontab -l
Expected Output:
If no jobs are scheduled, the output will be empty.

Task 2: Scheduling a Simple Cron Job

Subtask 2.1: Create a Test Script

Create a script ~/test_cron.sh:
#!/bin/bash
echo "Cron job executed at $(date)" >> ~/cron_test.log
Make it executable:
chmod +x ~/test_cron.sh
Subtask 2.2: Schedule the Script to Run Every Minute

Open the crontab editor:
crontab -e
Add the following line to run the script every minute:
* * * * * ~/test_cron.sh
Save and exit (in nano, press Ctrl+O, Enter, then Ctrl+X).
Expected Outcome:
After a minute, check ~/cron_test.log:

cat ~/cron_test.log
You should see timestamps logged every minute.

Task 3: Scheduling System Maintenance Tasks

Subtask 3.1: Schedule a Daily Backup

Create a backup script ~/daily_backup.sh:
#!/bin/bash
tar -czf ~/backups/backup_$(date +\%Y\%m\%d).tar.gz /path/to/important_files
Make it executable:
chmod +x ~/daily_backup.sh
Schedule it to run daily at 2 AM:
0 2 * * * ~/daily_backup.sh
Subtask 3.2: Verify the Backup Job

Check the cron log to confirm execution:

grep CRON /var/log/syslog
Expected Outcome:
Log entries showing the backup job running at 2 AM.

Task 4: Automating Log Cleanup

Subtask 4.1: Write a Log Cleanup Script

Create ~/cleanup_logs.sh:
#!/bin/bash
find /var/log -name "*.log" -type f -mtime +7 -exec rm -f {} \;
This script deletes log files older than 7 days.

Make it executable:
chmod +x ~/cleanup_logs.sh
Subtask 4.2: Schedule Daily Log Cleanup

Add to crontab:
0 3 * * * ~/cleanup_logs.sh
This runs the cleanup daily at 3 AM.

Troubleshooting Tip:
If the script fails, ensure:

The user has permissions to /var/log.
Test the find command manually first.
