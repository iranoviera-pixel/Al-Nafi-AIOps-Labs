Lab 31: Networking with DHCP
Overview
This lab focuses on understanding and configuring Dynamic Host Configuration Protocol (DHCP) on an Ubuntu Linux system. The objective is to manage network interfaces, request dynamic IP addresses, and automate the renewal process through shell scripting.

Objectives
Identify active network interfaces.

Install and configure the DHCP client package (isc-dhcp-client).

Manually release and renew DHCP leases.

Create an automation script for network connectivity verification.

Technical Troubleshooting
During the lab, several connectivity hurdles were addressed:

Missing Package: The dhclient command was initially missing from the system.

Network Isolation: Attempted to install packages while the interface lacked an IP address and proper DNS resolution.

Resolution:

Used sudo netplan apply to trigger the default system network manager.

Verified the interface name as enp0s1 instead of the generic eth0.

Successfully updated the package repository and installed isc-dhcp-client once internet access was restored.

Tasks Performed
1. DHCP Lease Management (Subtask 2.1)

Release: Executed sudo dhclient -r enp0s1 to drop the current lease.

Request: Executed sudo dhclient enp0s1 to obtain a new IP address from the DHCP server.

Verification: Inspected /var/lib/dhcp/dhclient.leases to confirm the fixed address, subnet mask, and router details provided by the lab environment.

2. Automation Scripting

A custom bash script was created at /usr/local/bin/renew_dhcp.sh with the following functionality:

Sets the target interface specifically to enp0s1.

Automates the release and renewal process.

Displays the current IP configuration using ip a.

Performs a connectivity test via ping google.com to ensure the link is active.

Key Commands Reference
Bash
# View network interface details
ip a show enp0s1

# Apply Netplan configuration
sudo netplan apply

# Install DHCP client tools
sudo apt update && sudo apt install isc-dhcp-client -y

# View the DHCP lease history
sudo cat /var/lib/dhcp/dhclient.leases


