Lab 74: Basic Configuration and Real-world Scenario of Squid

Objectives

By the end of this lab, you will be able to:

Install and configure Squid Proxy Server with ACLs and caching rules.
Monitor Squid logs for troubleshooting and performance optimization.
Automate Squid configuration and log rotation using a Bash script.
Prerequisites

A Linux system (Ubuntu 20.04/22.04 or CentOS 7/8)
Root or sudo privileges
Basic knowledge of Linux command line and text editors (nano/vim)
Internet connectivity
Task 1: Install and Configure Squid with ACLs and Caching Rules

Subtask 1.1: Install Squid

Update your package repository:

sudo apt update  # For Ubuntu/Debian
sudo yum update  # For CentOS/RHEL
Install Squid:

sudo apt install squid -y  # Ubuntu/Debian
sudo yum install squid -y  # CentOS/RHEL
Start and enable Squid:

sudo systemctl start squid
sudo systemctl enable squid
Expected Outcome: Squid is installed and running. Verify with:

sudo systemctl status squid
Subtask 1.2: Configure Basic ACLs

Open the Squid configuration file:

sudo nano /etc/squid/squid.conf
Add the following ACL rules to restrict access to specific IP range (e.g., 192.168.1.0/24):

acl localnet src 192.168.1.0/24
http_access allow localnet
http_access deny all
Save and exit (Ctrl+O, Enter, Ctrl+X).

Restart Squid:

sudo systemctl restart squid
Expected Outcome: Only clients from 192.168.1.0/24 can access the proxy.

Subtask 1.3: Configure Caching

Edit /etc/squid/squid.conf again:

sudo nano /etc/squid/squid.conf
Set cache size and rules (e.g., 4GB cache):

cache_dir ufs /var/spool/squid 4000 16 256
maximum_object_size 256 MB
refresh_pattern . 1440 20% 10080
Restart Squid:

sudo systemctl restart squid
Expected Outcome: Squid will cache objects up to 256MB with optimized refresh patterns.

Task 2: Monitor Squid Logs and Optimize Configuration

Subtask 2.1: Monitor Access Logs

View real-time access logs:

sudo tail -f /var/log/squid/access.log
Filter logs by IP (e.g., 192.168.1.10):

sudo grep '192.168.1.10' /var/log/squid/access.log
Expected Outcome: You can monitor and filter proxy access requests.

Subtask 2.2: Optimize Configuration

Check Squid performance metrics:

sudo squidclient mgr:info
Tune the number of Squid workers (edit /etc/squid/squid.conf):

workers 4
Restart Squid:

sudo systemctl restart squid
Expected Outcome: Improved proxy performance with multiple workers.

Task 3: Automate Squid Configuration and Log Rotation

Subtask 3.1: Create a Log Rotation Script

Create a script /usr/local/bin/squid_logrotate.sh:

sudo nano /usr/local/bin/squid_logrotate.sh
Add the following content:

#!/bin/bash
LOG_DIR="/var/log/squid"
DATE=$(date +%Y%m%d)

# Rotate logs
mv $LOG_DIR/access.log $LOG_DIR/access_$DATE.log
mv $LOG_DIR/cache.log $LOG_DIR/cache_$DATE.log

# Restart Squid to create new logs
systemctl restart squid

# Compress old logs
gzip $LOG_DIR/*_$DATE.log
Make the script executable:

sudo chmod +x /usr/local/bin/squid_logrotate.sh
Expected Outcome: Logs are rotated and compressed daily.

Subtask 3.2: Schedule Log Rotation with Cron

Open the crontab editor:

sudo crontab -e
Add a daily log rotation job (runs at midnight):

0 0 * * * /usr/local/bin/squid_logrotate.sh
Expected Outcome: Automated daily log rotation.

