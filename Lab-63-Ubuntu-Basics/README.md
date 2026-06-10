Lab 63: Automating Firewall Rules with Scripts

Objectives

By the end of this lab, you will be able to:

Understand basic firewall management using iptables and firewalld
Create dynamic firewall rules through scripting
Automate IP blocking based on system activity
Schedule periodic firewall rule updates
Prerequisites

A Linux system (Ubuntu 20.04/CentOS 8 used in examples)
Basic command line proficiency
Sudo/root access
cron service installed
Text editor (nano/vim)
Task 1: Creating Dynamic Firewall Rules

Subtask 1.1: Choosing Your Firewall Tool

Linux offers two primary firewall solutions:

iptables (traditional)
firewalld (modern, default on RHEL/CentOS)
For iptables users:

sudo iptables -L  # View current rules
For firewalld users:

sudo firewall-cmd --list-all
Subtask 1.2: Creating Basic Rules

Example: Allow SSH (Port 22)

# iptables
sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# firewalld
sudo firewall-cmd --add-service=ssh --permanent
sudo firewall-cmd --reload
Expected Outcome: SSH connections remain allowed while other traffic is restricted.

Task 2: Scripting IP Blocking

Subtask 2.1: Creating IP Block Script

Create /usr/local/bin/block_malicious.sh:

#!/bin/bash

# Define threshold (number of connections)
THRESHOLD=100

# Get IPs exceeding threshold from netstat
BLOCK_IPS=$(netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n | awk -v limit=$THRESHOLD '$1 > limit {print $2}')

# Block each IP
for IP in $BLOCK_IPS
do
    echo "Blocking $IP"
    # iptables
    iptables -A INPUT -s $IP -j DROP
    
    # firewalld alternative
    # firewall-cmd --add-rich-rule="rule family='ipv4' source address='$IP' reject" --permanent
done

# For firewalld users
# firewall-cmd --reload
Make it executable:

sudo chmod +x /usr/local/bin/block_malicious.sh
Subtask 2.2: Testing the Script

Run manually first:

sudo /usr/local/bin/block_malicious.sh
Check blocked IPs:

sudo iptables -L INPUT -v -n
# OR
sudo firewall-cmd --list-rich-rules
Troubleshooting Tip: If script fails, check:

Netstat output format may vary - adjust awk commands accordingly
Ensure you have write permissions to firewall rules
Task 3: Automating Rule Updates

Subtask 3.1: Scheduling with Cron

Edit crontab:

sudo crontab -e
Add this line to run hourly:

0 * * * * /usr/local/bin/block_malicious.sh
Subtask 3.2: Logging Activity

Enhance script with logging:

#!/bin/bash

LOG_FILE="/var/log/firewall_autoblock.log"
THRESHOLD=100

{
    date
    echo "Checking for malicious IPs..."
    
    BLOCK_IPS=$(netstat -ntu | awk '{print $5}' | cut -d: -f1 | sort | uniq -c | sort -n | awk -v limit=$THRESHOLD '$1 > limit {print $2}')
    
    [ -z "$BLOCK_IPS" ] && echo "No IPs to block" && exit 0
    
    for IP in $BLOCK_IPS
    do
        echo "Blocking $IP"
        iptables -A INPUT -s $IP -j DROP
        # firewall-cmd alternative here if needed
    done
    
    echo "Blocking complete"
} >> $LOG_FILE 2>&1
Expected Outcome: The script will run hourly, blocking suspicious IPs and logging activity to /var/log/firewall_autoblock.log.

