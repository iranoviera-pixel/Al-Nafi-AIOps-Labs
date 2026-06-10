Lab 55: Configuring a DHCP Server

Objectives

By the end of this lab, you will be able to:

Install and configure a DHCP server on a Linux system
Define and manage IP address pools for client devices
Create a basic DHCP configuration file with essential parameters
Automate DHCP server setup using a Bash script
Verify DHCP server functionality
Prerequisites

A Linux system (Ubuntu 20.04/22.04 or CentOS 7/8 recommended)
Root or sudo privileges
Basic understanding of networking concepts (IP addressing, subnets)
A text editor (nano/vim)
Network interface configured with static IP (for the DHCP server)
Task 1: Install and Configure DHCP Server

Subtask 1.1: Install DHCP Server Package

# For Ubuntu/Debian
sudo apt update
sudo apt install isc-dhcp-server -y

# For CentOS/RHEL
sudo yum install dhcp -y
Verification:

# Check installation
dhcpd --version
Expected Output:
ISC DHCP Server X.X.X

Subtask 1.2: Configure DHCP Server

Edit the main configuration file:

sudo nano /etc/dhcp/dhcpd.conf
Add the following basic configuration (adjust values as needed):

# Global settings
option domain-name "example.com";
option domain-name-servers 8.8.8.8, 8.8.4.4;
default-lease-time 600;
max-lease-time 7200;
authoritative;

# Subnet declaration
subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.100 192.168.1.200;
  option routers 192.168.1.1;
  option broadcast-address 192.168.1.255;
}
Key Parameters Explained:

range: IP address pool for clients
routers: Default gateway
domain-name-servers: DNS servers
Subtask 1.3: Specify Network Interface

Edit the DHCP server defaults file:

sudo nano /etc/default/isc-dhcp-server
Set the interface:

INTERFACESv4="eth0"
Troubleshooting Tip:
Use ip a to verify your network interface name.

Subtask 1.4: Start and Enable DHCP Service

sudo systemctl start isc-dhcp-server  # Ubuntu/Debian
sudo systemctl start dhcpd            # CentOS/RHEL

sudo systemctl enable isc-dhcp-server  # Enable at boot
Verification:

sudo systemctl status isc-dhcp-server
Task 2: Test DHCP Functionality

Subtask 2.1: Lease File Inspection

sudo cat /var/lib/dhcp/dhcpd.leases
Subtask 2.2: Client Test

On a client machine in the same network:

sudo dhclient -v eth0
Expected Outcome:
Client receives an IP from your defined range (192.168.1.100-200).

Task 3: Automation Script

Subtask 3.1: Create DHCP Setup Script

#!/bin/bash
# dhcp_auto_setup.sh

# Install DHCP Server
if [ -f /etc/debian_version ]; then
    apt update && apt install -y isc-dhcp-server
elif [ -f /etc/redhat-release ]; then
    yum install -y dhcp
fi

# Basic Configuration
cat > /etc/dhcp/dhcpd.conf <<EOF
option domain-name "example.com";
option domain-name-servers 8.8.8.8, 8.8.4.4;
default-lease-time 600;
max-lease-time 7200;
authoritative;

subnet 192.168.1.0 netmask 255.255.255.0 {
  range 192.168.1.100 192.168.1.200;
  option routers 192.168.1.1;
}
EOF

# Start Service
systemctl start isc-dhcp-server || systemctl start dhcpd
systemctl enable isc-dhcp-server || systemctl enable dhcpd

echo "DHCP Server configured successfully!"
Subtask 3.2: Make Script Executable and Run

chmod +x dhcp_auto_setup.sh
sudo ./dhcp_auto_setup.sh
Conclusion

In this lab you have:

Successfully installed and configured an ISC DHCP server
Created a functional IP address allocation system
Developed an automation script for rapid deployment
Verified proper DHCP operation through client testing
Key Takeaways:

DHCP dramatically simplifies network administration
Configuration files control all critical parameters
Automation scripts ensure consistent deployments
Next Steps:

Explore advanced DHCP options like static reservations
Implement DHCP relay for multi-subnet environments
Set up logging for lease monitoring
Troubleshooting Guide

Issue	Solution
Service fails to start	Check /var/log/syslog (Ubuntu) or /var/log/messages (CentOS)
Clients not getting IPs	Verify firewall isn't blocking UDP ports 67/68
Invalid configuration	Run dhcpd -t to test config file syntax
Useful Commands:

# Test configuration syntax
sudo dhcpd -t -cf /etc/dhcp/dhcpd.conf

# Release all leases
sudo rm /var/lib/dhcp/dhcpd.leases*
