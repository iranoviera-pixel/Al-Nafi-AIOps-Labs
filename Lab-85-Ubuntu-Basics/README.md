Lab 85: NRPE Process and Port Understanding

Objectives

By the end of this lab, you will be able to:

Understand how NRPE (Nagios Remote Plugin Executor) communicates with Nagios
Check NRPE service status and port using Linux commands
Write a basic script to monitor NRPE service availability
Prerequisites:
Basic Linux command line knowledge
A Linux system with NRPE installed (Ubuntu/CentOS)
Nagios server (or basic understanding of Nagios monitoring)
Net-tools package installed (netstat)
Lab Tasks

Task 1: Research NRPE Communication with Nagios

Subtask 1.1: Understand NRPE Architecture

NRPE allows Nagios to execute plugins on remote Linux/Unix machines. The communication flow:

Nagios server sends check request to NRPE daemon on client
NRPE executes local plugins and returns results to Nagios
Communication happens via TCP port 5666 by default)
Subtask 1.2: Verify NRPE Installation

# Check if NRPE is installed
which check_nrpe

# Expected output:
# /usr/local/nagios/libexec/check_nrpe
# OR
# /usr/bin/check_nrpe
Subtask 1.3: Check NRPE Configuration

# View NRPE configuration file
sudo cat /etc/nagios/nrpe.cfg

# Key parameters to note:
# server_address - IP NRPE binds to
# allowed_hosts - Nagios servers allowed to connect
# command - Plugin definitions
Task 2: Check NRPE Port Using netstat

Subtask 2.1: Install net-tools (if needed)

# For Ubuntu/Debian:
sudo apt install net-tools -y

# For CentOS/RHEL:
sudo yum install net-tools -y
Subtask 2.2: Check NRPE Port Status

# Check if NRPE is listening on port 5666
sudo netstat -tulnp | grep nrpe

# Expected output:
# tcp        0      0 0.0.0.0:5666            0.0.0.0:*               LISTEN      1234/nrpe
Subtask 2.3: Verify Connectivity

# Test connection from localhost
/usr/local/nagios/libexec/check_nrpe -H 127.0.0.1

# Expected output:
# NRPE v3.2.1
Troubleshooting Tip: If connection fails:

Check if NRPE service is running: sudo systemctl status nrpe
Verify firewall rules: sudo iptables -L
Task 3: Create NRPE Monitoring Script

Subtask 3.1: Script to Check NRPE Service

Create check_nrpe_service.sh:

#!/bin/bash

# Check if NRPE process is running
if pgrep -x "nrpe" > /dev/null
then
    echo "NRPE service is running"
else
    echo "NRPE service is NOT running"
    exit 1
fi

# Check port 5666 connectivity
if nc -zv localhost 5666 2>&1 | grep -q "succeeded"
then
    echo "NRPE port 5666 is accessible"
else
    echo "NRPE port is NOT accessible"
    exit 1
fi
Subtask 3.2: Make Script Executable

chmod +x check_nrpe_service.sh
Subtask 3.3: Test the Script

./check_nrpe_service.sh

# Expected output (success case):
# NRPE service is running
# NRPE port 5666 is accessible
Subtask 3.4: Schedule Regular Checks (Optional)

# Add to crontab to run every 5 minutes
(crontab -l 2>/dev/null; echo "*/5 * * * * /path/to/check_nrpe_service.sh >> /var/log/nrpe_monitor.log") | crontab -
