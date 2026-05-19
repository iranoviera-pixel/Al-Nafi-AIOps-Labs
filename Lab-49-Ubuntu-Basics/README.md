Lab 49: Time Synchronization with Chrony

Objectives

By the end of this lab, you will be able to:

Install and configure Chrony for accurate time synchronization on Linux systems.
Verify time synchronization status using chronyc commands.
Automate Chrony startup and synchronization with a custom script.
Prerequisites

A Linux system (Ubuntu/CentOS/RHEL)
Terminal access with sudo/root privileges
Internet connectivity (to sync with NTP servers)
Task 1: Install and Configure Chrony

Subtask 1.1: Install Chrony

Open a terminal and run the following command based on your distribution:

For Ubuntu/Debian:

sudo apt update && sudo apt install chrony -y
For CentOS/RHEL:

sudo yum install chrony -y
Expected Output:
Package installation completes without errors.

Subtask 1.2: Configure Chrony

Edit the Chrony configuration file:

sudo nano /etc/chrony/chrony.conf
Add/replace the NTP server pool (e.g., NTP servers for the USA):

server 0.us.pool.ntp.org iburst
server 1.us.pool.ntp.org iburst
server 2.us.pool.ntp.org iburst
server 3.us.pool.ntp.org iburst
Save the file (Ctrl+O, Enter, Ctrl+X).

Restart Chrony to apply changes:

sudo systemctl restart chrony
Troubleshooting Tip:
If Chrony fails to start, check logs with:

journalctl -u chrony
Task 2: Verify Time Synchronization

Subtask 2.1: Check Synchronization Status

Run the following command:

chronyc tracking
Expected Output:
Displays details like reference ID, stratum, and time offset.
Example:

Reference ID    : A29FC87B (0.us.pool.ntp.org)
Stratum         : 2
Ref time (UTC)  : Thu Oct 05 14:23:45 2023
System time     : 0.000123 seconds slow of NTP time
Subtask 2.2: Verify Active Servers

List active NTP servers:

chronyc sources -v
Key Concept:
^* indicates a synchronized server. Ensure at least one server is marked with ^*.

Task 3: Automate Chrony with a Script

Subtask 3.1: Create a Startup Script

Create a script file:

sudo nano /usr/local/bin/chrony_sync.sh
Add the following content:

#!/bin/bash
# Ensure Chrony is running and synced
systemctl start chrony
chronyc waitsync 30  # Wait up to 30 seconds for sync
echo "Time synchronized: $(date)"
Make the script executable:

sudo chmod +x /usr/local/bin/chrony_sync.sh
Subtask 3.2: Schedule the Script

Add a cron job to run at boot:

sudo crontab -e
Add this line to the crontab:

@reboot /usr/local/bin/chrony_sync.sh
Verification:
Reboot the system and check sync status with chronyc tracking
