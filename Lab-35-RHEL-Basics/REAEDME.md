Configuring firewalld Zones and Services

Objectives

By the end of this lab, students will be able to:

Understand the concept of firewalld zones and services.
Create and manage custom firewalld zones using firewall-cmd.
Add and remove services from zones to control network traffic.
Automate firewall configurations using a Bash script.
Prerequisites

Before starting this lab, ensure you have:

A Linux-based system with firewalld installed (provided by Al Nafi's cloud machines).
Basic familiarity with the Linux command line.
Sudo or root privileges to modify firewall settings.
Note: Al Nafi provides pre-configured Linux cloud machines. Click Start Lab to begin—no VM setup required!

Task 1: Create Custom firewalld Zones

Step 1: Check firewalld Status

Open a terminal.
Run the following command to verify firewalld is active:
sudo systemctl status firewalld
Expected Output: Active (running) status.
Troubleshooting: If inactive, start it with sudo systemctl start firewalld.
Step 2: List Existing Zones

View default zones:
sudo firewall-cmd --get-zones
Expected Output: A list like public, work, home, etc..
Step 3: Create a Custom Zone

Create a zone named lab_zone:
sudo firewall-cmd --permanent --new-zone=lab_zone
Reload the firewall to apply changes:
sudo firewall-cmd --reload
Verify the new zone:
sudo firewall-cmd --get-zones | grep lab_zone
Expected Output: lab_zone appears in the list.
Task 2: Add and Remove Services from a Zone

Step 1: List Available Services

View predefined services:
sudo firewall-cmd --get-services
Example Output: http, ssh, dhcp.
Step 2: Add a Service to the Zone

Allow HTTP traffic in lab_zone:
sudo firewall-cmd --permanent --zone=lab_zone --add-service=http
Reload the firewall:
sudo firewall-cmd --reload
Verify:
sudo firewall-cmd --zone=lab_zone --list-services
Expected Output: http appears.
Step 3: Remove a Service

Remove HTTP from lab_zone:
sudo firewall-cmd --permanent --zone=lab_zone --remove-service=http
Reload and verify:
sudo firewall-cmd --reload
sudo firewall-cmd --zone=lab_zone --list-services
Expected Output: http is no longer listed.
Task 3: Automate Zone/Service Configuration with a Script

Step 1: Create a Bash Script

Open a text editor and create firewall_setup.sh:
#!/bin/bash
# Define zone and services
ZONE="secure_lab"
SERVICES=("http" "https" "ssh")

# Create zone
sudo firewall-cmd --permanent --new-zone=$ZONE

# Add services
for service in "${SERVICES[@]}"; do
    sudo firewall-cmd --permanent --zone=$ZONE --add-service=$service
done

# Reload firewall
sudo firewall-cmd --reload
echo "Zone '$ZONE' configured with services: ${SERVICES[*]}"
Step 2: Make the Script Executable

Set permissions:
chmod +x firewall_setup.sh
Step 3: Run the Script

Execute the script:
./firewall_setup.sh
Expected Output: Confirmation message and the new zone with services.
