Lab 41: Advanced firewalld Rules

Objectives

By the end of this lab, students will be able to:

Create and manage firewalld zones and services.
Configure advanced traffic filtering rules based on IP, port, and protocol.
Automate firewalld rule deployment using scripts.
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge (e.g., sudo, vim, systemctl).
A Linux-based machine with firewalld installed (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Administrative access (use sudo where required).
Task 1: Create Custom firewalld Zones and Configure Services

Step 1: Check firewalld Status

Open a terminal.
Run:
sudo systemctl status firewalld
Expected Output: Active (running).
Troubleshooting: If inactive, start it with sudo systemctl start firewalld.
Step 2: Create a Custom Zone

Create a zone named lab-zone:
sudo firewall-cmd --permanent --new-zone=lab-zone
Reload firewalld to apply changes:
sudo firewall-cmd --reload
Verify the zone exists:
sudo firewall-cmd --get-zones
Expected Output: lab-zone appears in the list.
Step 3: Add Services to the Zone

Allow HTTP traffic in lab-zone:
sudo firewall-cmd --permanent --zone=lab-zone --add-service=http
Reload and verify:
sudo firewall-cmd --reload
sudo firewall-cmd --zone=lab-zone --list-services
Expected Output: http appears in the services list.
Task 2: Write Advanced Traffic Filtering Rules

Step 1: Block Traffic from a Specific IP

Block all traffic from IP 192.168.1.100:
sudo firewall-cmd --permanent --zone=lab-zone --add-rich-rule='rule family="ipv4" source address="192.168.1.100" reject'
Explanation: The reject action sends a rejection message to the sender.
Step 2: Allow Traffic on a Non-Standard Port

Allow TCP traffic on port 8080:
sudo firewall-cmd --permanent --zone=lab-zone --add-port=8080/tcp
Step 3: Restrict Protocol (ICMP Example)

Block ICMP (ping) in lab-zone:
sudo firewall-cmd --permanent --zone=lab-zone --add-icmp-block=echo-request
Reload and verify all rules:
sudo firewall-cmd --reload
sudo firewall-cmd --zone=lab-zone --list-all
Expected Output: Rules for IP, ports, and ICMP appear under lab-zone.
Task 3: Automate Rule Creation with a Script

Step 1: Create a Script

Open a file named firewall-setup.sh:
vim firewall-setup.sh
Paste the following script:
#!/bin/bash
# Create a zone and add rules
sudo firewall-cmd --permanent --new-zone=auto-zone
sudo firewall-cmd --permanent --zone=auto-zone --add-service=ssh
sudo firewall-cmd --permanent --zone=auto-zone --add-port=3306/tcp
sudo firewall-cmd --permanent --zone=auto-zone --add-rich-rule='rule family="ipv4" source address="10.0.0.5" accept'
# Apply changes
sudo firewall-cmd --reload
echo "Firewall rules applied successfully!"
Step 2: Run the Script

Make the script executable:
chmod +x firewall-setup.sh
Execute it:
./firewall-setup.sh
Expected Output: "Firewall rules applied successfully!"
