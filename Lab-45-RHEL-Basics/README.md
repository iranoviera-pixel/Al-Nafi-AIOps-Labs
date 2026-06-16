Lab 45: Troubleshooting SELinux Denials

Objectives

By the end of this lab, you will be able to:

Analyze SELinux denials using sealert.
Identify the root causes of denials by examining /var/log/audit/audit.log.
Create a basic script to monitor SELinux denials and alert administrators.
Prerequisites

Before starting, ensure you have:

A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with the Linux command line.
Administrative (root) access to install packages (sudo privileges).
SELinux installed and running in enforcing mode (default on RHEL/CentOS/Fedora).
Task 1: Use sealert to Analyze SELinux Denials

Step 1: Install Required Tools

Install the setroubleshoot package (includes sealert):

sudo dnf install setroubleshoot -y  # For RHEL/CentOS/Fedora
sudo apt-get install setroubleshoot -y  # For Debian/Ubuntu
Step 2: Generate a Test Denial

Trigger a denial for practice (e.g., try moving a file to /etc):

touch testfile
sudo mv testfile /etc/  # This will likely be denied by SELinux
Step 3: Analyze the Denial

Run sealert to view the most recent denial:

sudo sealert -a /var/log/audit/audit.log
Expected Output: A detailed report explaining the denial, including:
Cause: Why the action was blocked.
Solution: Suggested fixes (e.g., changing file context or adjusting policies).
Troubleshooting Tip

If sealert returns no output, ensure SELinux is enforcing:

sudo setenforce 1  # Switch to enforcing mode if not already
Task 2: Examine audit.log for Denial Causes

Step 1: Locate the Denial in audit.log

View the last 10 entries in the audit log:

sudo tail -n 10 /var/log/audit/audit.log
Look for lines containing avc: denied.
Step 2: Decode the Denial

Use ausearch to filter SELinux denials:

sudo ausearch -m avc -ts recent
Key Fields to Note:
scontext: Source context (e.g., process trying to access a file).
tcontext: Target context (e.g., file/directory being accessed).
tclass: Object type (e.g., file, dir).
Step 3: Resolve the Issue

Example: If the denial involves Apache (httpd) accessing a file, adjust the file context:

sudo chcon -t httpd_sys_content_t /path/to/file
Task 3: Script to Monitor SELinux Denials

Step 1: Create a Monitoring Script

Write a script (denial_monitor.sh) to alert on new denials:

#!/bin/bash
LOG_FILE="/var/log/audit/audit.log"
ALERT_EMAIL="admin@example.com"

# Check for new denials
NEW_DENIALS=$(sudo ausearch -m avc -ts recent)

if [ -n "$NEW_DENIALS" ]; then
    echo "New SELinux denials detected:" | mail -s "SELinux Alert" "$ALERT_EMAIL"
    echo "$NEW_DENIALS" | mail -s "SELinux Denial Details" "$ALERT_EMAIL"
fi
Step 2: Make the Script Executable

chmod +x denial_monitor.sh
Step 3: Schedule Regular Checks with Cron

Add a cron job to run the script hourly:

(crontab -l 2>/dev/null; echo "0 * * * * /path/to/denial_monitor.sh") | crontab -
Expected Outcome

The script will email the administrator if new denials are found in audit.log.
