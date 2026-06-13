Automating firewalld Configuration

Objectives

By the end of this lab, students will be able to:

Understand firewalld zones and services.
Write a Bash script to automate firewalld configurations.
Schedule scripts to run at boot using systemd.
Apply firewall rules to specific network interfaces.
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge (e.g., ls, cd, nano).
A Linux system with firewalld installed (Al Nafi’s cloud machine provides this).
Root/sudo access to modify firewall settings.
Note: Al Nafi provides pre-configured Linux cloud machines. Click Start Lab to begin—no VM setup required!

Task 1: Configure firewalld Zones for Network Interfaces

Step 1: Check Existing firewalld Configuration

Open a terminal.
Run:
sudo firewall-cmd --list-all-zones
Expected Output: Lists all zones (e.g., public, home, internal) and their settings.
Step 2: Create a Script to Assign Zones to Interfaces

Create a script file:

nano firewall_setup.sh
Add the following script (explanation below):

#!/bin/bash
# Assign zones to network interfaces
firewall-cmd --permanent --zone=public --change-interface=eth0
firewall-cmd --permanent --zone=internal --change-interface=eth1
firewall-cmd --reload
echo "Zones assigned to interfaces."
Explanation:
--permanent: Saves changes across reboots.
--zone: Specifies the zone (e.g., public for external traffic, internal for trusted networks).
--change-interface: Binds the zone to the interface (e.g., eth0, eth1).
Save (Ctrl+O) and exit (Ctrl+X).

Step 3: Make the Script Executable

chmod +x firewall_setup.sh
Step 4: Run the Script

sudo ./firewall_setup.sh
Expected Outcome: Interfaces eth0 and eth1 are assigned to public and internal zones, respectively.
Task 2: Automate Adding/Removing Services to Zones

Step 1: Script to Manage Services

Edit firewall_setup.sh:
nano firewall_setup.sh
Append these lines:
# Allow HTTP in public zone, block SSH in internal zone
firewall-cmd --permanent --zone=public --add-service=http
firewall-cmd --permanent --zone=internal --remove-service=ssh
firewall-cmd --reload
echo "Services updated in zones."
Step 2: Verify Changes

sudo firewall-cmd --zone=public --list-services
Expected Output: http appears in the public zone.
Task 3: Schedule Script to Run on Boot

Step 1: Create a systemd Service

Create a service file:
sudo nano /etc/systemd/system/firewall-config.service
Add:
[Unit]
Description=Configure firewalld at boot
After=network.target

[Service]
ExecStart=/path/to/firewall_setup.sh

[Install]
WantedBy=multi-user.target
Replace /path/to/ with the actual script path (e.g., /home/user/).
Step 2: Enable the Service

sudo systemctl enable firewall-config.service
sudo systemctl start firewall-config.service
Step 3: Test Reboot (Optional)

sudo reboot
Verification: After reboot, run sudo firewall-cmd --list-all-zones to confirm settings persist.
Troubleshooting Tips

Error: "Zone already set": Use --change-interface to override.
Service not found: Ensure the service name is valid (firewall-cmd --get-services).
Permission denied: Run scripts with sudo.
