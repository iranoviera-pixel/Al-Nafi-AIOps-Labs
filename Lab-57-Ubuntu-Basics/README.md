Lab 57: Introduction to Firewall

Objectives

By the end of this lab, you will be able to:

Understand the role of firewalls in Linux security
Check the status of a firewall using ufw or firewalld
Create and implement basic firewall rules to secure a Linux system
Write a script to automate firewall configuration
Prerequisites

A Linux system (Ubuntu/Debian for ufw, CentOS/RHEL for firewalld)
Basic knowledge of Linux command line
Sudo or root privileges
Task 1: Research the Role of Firewalls in Linux Security

Subtask 1.1: Understanding Firewalls

A firewall is a network security system that monitors and controls incoming and outgoing network traffic based on predetermined security rules. In Linux, common firewall solutions include:

ufw (Uncomplicated Firewall): Default on Ubuntu/Debian
firewalld: Default on CentOS/RHEL
Concepts to Research:

Packet Filtering: Blocks or allows packets based on rules.
Stateful Inspection: Tracks active connections to allow only legitimate traffic.
Zones (firewalld): Defines trust levels for network interfaces.
Expected Outcome: Understand how firewalls enhance Linux security.

Task 2: Check the Status of the Firewall

Subtask 2.1: Using ufw (Ubuntu/Debian)

Check if ufw is installed:

sudo ufw status
If inactive, enable it:
sudo ufw enable
View detailed status:

sudo ufw status verbose
Expected Output:

Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing)
Subtask 2.2: Using firewalld (CentOS/RHEL)

Check status:

sudo systemctl status firewalld
Enable and start firewalld:

sudo systemctl enable --now firewalld
List active zones:

sudo firewall-cmd --list-all
Expected Output:

public (active)
  target: eth0
  services: ssh dhcpv6-client
Troubleshooting Tip:
If firewalld is not installed, install it via:

sudo yum install firewalld -y  # CentOS/RHEL
Task 3: Write a Script to Configure Basic Firewall Rules

Subtask 3.1: Script for ufw (Ubuntu/Debian)

Create a script configure_ufw.sh:

#!/bin/bash

# Enable UFW
sudo ufw enable

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (port 22)
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS (ports 80, 443)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Reload rules
sudo ufw reload

# Display status
sudo ufw status verbose
Run the script:

chmod +x configure_ufw.sh
sudo ./configure_ufw.sh
Expected Outcome:
Firewall is active with SSH, HTTP, and HTTPS allowed.

Subtask 3.2: Script for firewalld (CentOS/RHEL)

Create a script configure_firewalld.sh:

#!/bin/bash

# Start and enable firewalld
sudo systemctl enable --now firewalld

# Add HTTP/HTTPS services
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https

# Allow SSH (port 22)
sudo firewall-cmd --permanent --add-service=ssh

# Reload firewall
sudo firewall-cmd --reload

# Display active rules
sudo firewall-cmd --list-all
Run the script:

chmod +x configure_firewalld.sh
sudo ./configure_firewalld.sh
Expected Outcome:
Firewall is active with SSH, HTTP, and HTTPS services enabled.

