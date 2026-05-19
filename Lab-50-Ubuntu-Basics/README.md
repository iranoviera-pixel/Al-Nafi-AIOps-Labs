Lab 50: Configuring SSH for Remote Access

Objectives

By the end of this lab, you will be able to:

Install and configure the OpenSSH server on a Linux system.
Manage the SSH service using systemctl.
Automate SSH server configuration and firewall rules using a Bash script.
Verify SSH connectivity between systems.
Prerequisites

A Linux-based system (Ubuntu 22.04/CentOS 8 or later recommended)
Sudo or root privileges
Basic familiarity with Linux command line
Network connectivity (to test remote access)
Task 1: Install and Configure OpenSSH Server

Step 1.1: Install OpenSSH Server

Update the package repository:

sudo apt update  # For Debian/Ubuntu
or

sudo dnf update  # For CentOS/RHEL
Install the OpenSSH server package:

sudo apt install openssh-server -y  # Debian/Ubuntu
or

sudo dnf install openssh-server -y  # CentOS/RHEL
Expected Outcome:
OpenSSH server is installed without errors. Verify with:

ssh -V
Step 1.2: Configure SSH Server

Open the SSH configuration file for editing:

sudo nano /etc/ssh/sshd_config
Modify the following settings for security (uncomment/edit lines):

Port 22                   # Default SSH port (change to a custom port if needed)
PermitRootLogin no        # Disable root login
PasswordAuthentication yes # Allow password auth (set to 'no' for key-only)
X11Forwarding no          # Disable X11 forwarding (unless needed)
Save the file (Ctrl+O, Enter, Ctrl+X).

Troubleshooting Tip:
If you change the default port, ensure the firewall allows traffic on the new port (covered in Task 3).

Task 2: Start and Enable SSH Service

Step 2.1: Start SSH Service

sudo systemctl start sshd    # For `sshd` (CentOS/RHEL)
or

sudo systemctl start ssh     # For `ssh` (Debian/Ubuntu)
Step 2.2: Enable SSH to Start on Boot

sudo systemctl enable sshd   # CentOS/RHEL
or

sudo systemctl enable ssh    # Debian/Ubuntu
Step 2.3: Verify SSH Status

sudo systemctl status sshd
Expected Outcome:
Active (running) status with "enabled" in the output.

Task 3: Automate SSH Configuration with a Script

Step 3.1: Create a Bash Script

Create a script file:

nano ssh_setup.sh
Paste the following script (customize as needed):

#!/bin/bash

# Update system and install OpenSSH
sudo apt update && sudo apt install openssh-server -y

# Backup original SSH config
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Configure SSH (disable root login, change port, etc.)
sudo sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config
sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config

# Configure firewall (UFW for Ubuntu)
sudo ufw allow 2222/tcp
sudo ufw enable

# Restart SSH service
sudo systemctl restart sshd

echo "SSH configured on port 2222. Root login disabled."
Make the script executable:

chmod +x ssh_setup.sh
Run the script:

./ssh_setup.sh
Expected Outcome:

SSH server listens on port 2222.
Root login is disabled.
Firewall rules are updated.
Verification Steps

Test SSH connectivity from another machine:
ssh username@<server_ip> -p 2222
Confirm root login` is blocked:
ssh root@<server_ip> -p 2222
Expected Error: Permission denied (publickey).
