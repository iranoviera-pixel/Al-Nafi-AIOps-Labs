Lab 77: Introduction to Failover

Objectives

By the end of this lab, you will:

Understand the concept of failover in networking.
Learn how to configure network interface failover using open-source tools (ifenslave or nmcli).
Develop a script to simulate and verify failover functionality.
Prerequisites

A Linux system (Ubuntu 20.04/CentOS 8 or later recommended).
Two or more physical/virtual network interfaces (eth0, eth1, etc.).
Root or sudo privileges.
Basic familiarity with Linux command line and networking.
Task 1: Research Failover Mechanisms for Network Interfaces

Subtask 1.1: Understand Failover Concepts

Key Concepts:

Failover: Automatic switching to a redundant/standby system upon failure of the primary interface.
Bonding/Link Aggregation: Combines multiple interfaces into a single logical interface for redundancy/load balancing.
Research Steps:

Review Linux bonding modes (mode=1 for active-backup, commonly used for failover).
Explore ifenslave (legacy) and nmcli (modern) tools for configuration.
Expected Outcome:

Clear understanding of failover mechanisms and bonding modes.
Task 2: Set Up a Failover Interface Group

Subtask 2.1: Install Required Tools

# Ubuntu/Debian
sudo apt update && sudo apt install -y ifenslave net-tools

# RHEL/CentOS
sudo dnf install -y NetworkManager-team
Subtask 2.2: Configure Failover Using nmcli (Recommended)

Create a bond interface with active-backup mode:
sudo nmcli connection add type bond con-name bond0 ifname bond0 mode active-backup
Add slave interfaces (e.g., eth0 and eth1):
sudo nmcli connection add type bond-slave ifname eth0 master bond0
sudo nmcli connection add type bond-slave ifname eth1 master bond0
Activate the bond:
sudo nmcli connection up bond0
Verification:

cat /proc/net/bonding/bond0  # Check bond status
ip link show bond0           # Verify interface state
Troubleshooting:

If interfaces fail to bind, ensure they are not managed by other services (e.g., disable NetworkManager conflicts).
Subtask 2.3: (Optional) Configure Failover Using ifenslave

Load the bonding kernel module:
sudo modprobe bonding
Edit /etc/network/interfaces (Debian) or /etc/sysconfig/network-scripts/ifcfg-bond0 (RHEL):
auto bond0
iface bond0 inet dhcp
    bond-mode active-backup
    bond-slaves eth0 eth1
    bond-miimon 100
Restart networking:
sudo systemctl restart networking  # Debian
sudo systemctl restart network     # RHEL
Task 3: Simulate and Verify Failover

Subtask 3.1: Write a Failover Test Script

Create failover_test.sh:

#!/bin/bash
echo "Current active interface:"
cat /proc/net/bonding/bond0 | grep "Active Slave" | awk '{print $4}'

echo "Disabling eth0..."
sudo ifconfig eth0 down

echo "New active interface:"
cat /proc/net/bonding/bond0 | grep "Active Slave" | awk '{print $4}'

echo "Re-enabling eth0..."
sudo ifconfig eth0 up
Subtask 3.2: Execute and Verify

Make the script executable:
chmod +x failover_test.sh
Run the script:
./failover_test.sh
Expected Outcome:

The script shows the active interface switching from eth0 to eth1 after eth0 is disabled.
