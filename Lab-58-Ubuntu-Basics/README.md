Lab 58: Configuring Iptables and Firewalld

Objectives

By the end of this lab, you will:

Understand the fundamentals of iptables and firewalld in Linux.
Configure basic firewall rules using iptables to allow/block network traffic.
Write and execute a script to configure firewalld for a specific network interface.
Prerequisites

A Linux system (Ubuntu/CentOS/RHEL) with root/sudo access.
Basic familiarity with terminal commands.
A network interface to configure (e.g., eth0 or ens33).
Task 1: Learn the Basics of iptables and firewalld

Subtask 1.1: Understand iptables

Explanation:
iptables is a user-space utility for configuring Linux kernel firewall rules. It operates using tables (e.g., filter, nat) and chains (e.g., INPUT, OUTPUT).

Key Concepts:

Tables: Define the purpose of rules (e.g., filter for packet filtering).
Chains: Define when rules are applied (e.g., INPUT for incoming traffic).
Targets: Actions like ACCEPT, DROP, or REJECT.
Command to List Current Rules:

sudo iptables -L -v
Expected Output:
Displays the current firewall rules.

Subtask 1.2: Understand firewalld

Explanation:
firewalld is a dynamic firewall manager with support for zones (e.g., public, home) and services (e.g., http, ssh).

Key Commands:

sudo systemctl status firewalld      # Check firewalld status
sudo firewall-cmd --list-all        # List active rules
Task 2: Use iptables to Create Rules

Subtask 2.1: Allow SSH Traffic

Command:

sudo iptables -A INPUT -p tcp --dport 22 -j ACCEPT
Explanation:

-A INPUT: Append rule to the INPUT chain.
-p tcp: Protocol is TCP.
--dport 22: Destination port is 22 (SSH).
-j ACCEPT: Accept the packet.
Verify Rule:

sudo iptables -L INPUT -v
Subtask 2.2: Block ICMP (Ping) Requests

Command:

sudo iptables -A INPUT -p icmp -j DROP
Test:

ping localhost  # Should fail
Subtask 2.3: Save Rules Permanently

For Ubuntu/Debian:

sudo apt install iptables-persistent
sudo netfilter-persistent save
For CentOS/RHEL:

sudo service iptables save
Task 3: Configure firewalld via Script

Subtask 3.1: Create a Script

Script Name: configure_firewalld.sh

#!/bin/bash
# Configure firewalld for a network interface

INTERFACE="ens33"
ZONE="public"

# Ensure firewalld is running
sudo systemctl start firewalld
sudo systemctl enable firewalld

# Assign interface to zone
sudo firewall-cmd --permanent --change-zone=$INTERFACE --zone=$ZONE

# Allow HTTP/HTTPS and deny ICMP
sudo firewall-cmd --permanent --zone=$ZONE --add-service=http
sudo firewall-cmd --permanent --zone=$ZONE --add-service=https
sudo firewall-cmd --permanent --zone=$ZONE --add-icmp-block=echo-request

# Reload to apply changes
sudo firewall-cmd --reload

# Display final configuration
echo "Firewall configuration for $INTERFACE:"
sudo firewall-cmd --zone=$ZONE --list-all
Subtask 3.2: Run the Script

chmod +x configure_firewalld.sh
sudo ./configure_firewalld.sh
Expected Outcome:

HTTP/HTTPS traffic allowed.
ICMP (ping) blocked.
Interface assigned to the public zone.
