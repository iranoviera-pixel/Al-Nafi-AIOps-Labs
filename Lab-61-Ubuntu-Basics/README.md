Lab 61: Scanning and Dealing with Open Ports

Objectives

By the end of this lab, you will be able to:

Identify open ports on a local system using netstat and ss.
Perform port scanning on a remote system using nmap.
Automate port scanning and firewall rule application using a Bash script.
Apply firewall rules to block unwanted open ports.
Prerequisites

A Linux system (Ubuntu/CentOS recommended)
Basic familiarity with the command line
sudo or root access (for firewall modifications)
nmap installed (sudo apt install nmap for Ubuntu/Debian, sudo yum install nmap for CentOS/RHEL)
Task 1: Use netstat or ss to List Open Ports

Subtask 1.1: Listing Open Ports with netstat

Open a terminal.

Run the following command to list all listening ports:

sudo netstat -tuln
-t: Show TCP ports
-u: Show UDP ports
-l: Display listening ports
-n: Show numerical addresses (no DNS resolution)
Expected Output:
A list of open ports with their protocol (TCP/UDP), local address, and state (e.g., LISTEN).

(Optional) Filter for specific services (e.g., HTTP on port 80):

sudo netstat -tuln | grep :80
Subtask 1.2: Listing Open Ports with ss (Modern Alternative)

Run the following command:

sudo ss -tuln
Same flags as netstat but faster and more efficient.
Expected Output:
Similar to netstat but with improved performance.

Task 2: Use nmap to Scan Open Ports on a Remote System

Subtask 2.1: Basic nmap Scan

Install nmap if not already installed:

sudo apt install nmap  # Ubuntu/Debian
sudo yum install nmap  # CentOS/RHEL
Scan a remote system (replace <IP> with the target IP or domain):

nmap -sT <IP>
-sT: TCP connect scan (reliable but detectable).
Expected Output:
A list of open ports and associated services (e.g., 22/tcp open ssh).

Subtask 2.2: Aggressive Scan (OS & Service Detection)

Run an aggressive scan for deeper insights:

nmap -A <IP>
-A: Enables OS detection, version detection, and script scanning.
Expected Output:
Detailed information including OS guess, service versions, and open ports.

Task 3: Write a Script to Automate Port Scanning and Firewall Rules

Subtask 3.1: Create a Port Scanning Script

Open a text editor and create port_scanner.sh:

#!/bin/bash

TARGET_IP="$1"
LOG_FILE="scan_results.txt"

echo "Scanning $TARGET_IP..." > $LOG_FILE
nmap -sT $TARGET_IP >> $LOG_FILE

echo "Scan completed. Results saved in $LOG_FILE."
Make the script executable:

chmod +x port_scanner.sh
Run the script (replace <IP>):

./port_scanner.sh <IP>
Expected Output:
A file scan_results.txt containing the nmap scan results.

Subtask 3.2: Automate Firewall Rules (UFW)

Install ufw if not present:

sudo apt install ufw  # Ubuntu/Debian
sudo yum install ufw  # CentOS/RHEL (may require EPEL)
Modify the script to block unwanted ports (e.g., port 23/tcp):

#!/bin/bash

TARGET_IP="$1"
LOG_FILE="scan_results.txt"
UNWANTED_PORTS="23"  # Example: Telnet

echo "Scanning $TARGET_IP..." > $LOG_FILE
nmap -sT $TARGET_IP >> $LOG_FILE

# Block unwanted ports
for port in $UNWANTED_PORTS; do
    sudo ufw deny $port/tcp
    echo "Blocked port $port/tcp via UFW."
done

echo "Script execution complete."
Run the updated script:

./port_scanner.sh <IP>
Expected Output:
Unwanted ports (e.g., 23) are blocked via UFW, and a log file is generated.

