Monitoring Network Traffic with iftop and nmap

Objectives

By the end of this lab, students will be able to:

Install and use iftop to monitor real-time network bandwidth usage.
Perform basic network scanning using nmap to identify open ports on local and remote systems.
Write a simple Bash script to log network traffic statistics and port scan results.
Prerequisites

Before starting this lab, ensure you have:

A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with the Linux command line.
Internet access to install packages (iftop and nmap).
Task 1: Install and Use iftop for Real-Time Bandwidth Monitoring

Step 1: Install iftop

Open the terminal on your Linux machine.
Run the following command to install iftop:
sudo apt update && sudo apt install iftop -y
Expected Outcome: iftop is installed without errors.
Step 2: Run iftop

Execute iftop with sudo privileges to monitor all interfaces:
sudo iftop
Expected Outcome: A live display of network traffic (source/destination IPs, bandwidth usage).
Step 3: Interpret iftop Output

Key Columns:
TX: Outbound traffic (sent data).
RX: Inbound traffic (received data).
TOTAL: Cumulative bandwidth usage.
Troubleshooting Tip: If no traffic appears, ensure your machine has active network activity (e.g., open a webpage).
Task 2: Use nmap to Scan Open Ports

Step 1: Install nmap

Install nmap using:
sudo apt install nmap -y
Expected Outcome: nmap is ready to use.
Step 2: Scan Localhost

Scan your machine’s open ports:
nmap localhost
Expected Output: A list of open ports (e.g., 22 for SSH).
Step 3: Scan a Remote System

Replace <IP> with a target IP (e.g., scanme.nmap.org):
nmap scanme.nmap.org
Expected Outcome: A list of the remote system’s open ports (e.g., 80 for HTTP).
Note: Only scan systems you have permission to test.
Task 3: Script to Log Network Traffic and Port Scans

Step 1: Create a Script

Open a text editor (e.g., nano):
nano network_monitor.sh
Paste the following script:
#!/bin/bash
LOG_FILE="network_log_$(date +%Y%m%d).txt"

echo "=== Network Traffic (iftop) ===" >> $LOG_FILE
sudo iftop -t -s 5 >> $LOG_FILE  # Runs for 5 seconds

echo "=== Open Ports (nmap) ===" >> $LOG_FILE
nmap localhost >> $LOG_FILE

echo "Log saved to $LOG_FILE"
Explanation: Logs iftop output and nmap results to a dated file.
Step 2: Make the Script Executable

Set execute permissions:
chmod +x network_monitor.sh
Run the script:
./network_monitor.sh
Expected Outcome: A log file (e.g., network_log_20231201.txt) is created with traffic/scan data.
