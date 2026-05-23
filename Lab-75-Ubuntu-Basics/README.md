Lab 75: Introduction to Bonding and Teaming

Objectives

By the end of this lab, you will be able to:

Understand the concepts of network bonding and teaming in Linux
Configure network bonding using ip link and nmcli
Create a startup script to automate bonding configuration
Verify bonding interface functionality
Prerequisites

A Linux system (Ubuntu 20.04/CentOS 8 or newer recommended)
Root or sudo privileges
At least two physical or virtual network interfaces
Basic familiarity with Linux command line and networking concepts
Lab Setup

Ensure your system has multiple network interfaces:

ip link show
(Look for at least two interfaces besides lo, e.g., eth0, eth1)

Install required packages:

# For bonding (Ubuntu/Debian)
sudo apt install ifenslave

# For bonding (RHEL/CentOS)
sudo yum install teamd
Task 1: Research Network Bonding and Teaming Concepts

Subtask 1.1: Understand Bonding vs. Teaming

Bonding: Legacy Linux kernel method (bond driver)
Modes: balance-rr, active-backup, balance-xor, broadcast, 802.3ad, balance-tlb, balance-alb
Teaming: Newer alternative (libteam library)
More flexible and maintainable than bonding
Supports JSON configuration
Subtask 1.2: Common Use Cases

Load balancing
Fault tolerance
Increased bandwidth aggregation
Task 2: Configure Network Bonding

Subtask 2.1: Create a Bond Interface Using ip link

Create bond interface:

sudo ip link add bond0 type bond mode active-backup
Add slave interfaces:

sudo ip link set eth0 master bond0
sudo ip link set eth1 master bond0
Bring up the bond interface:

sudo ip link set bond0 up
Assign an IP address (replace with your network values):

sudo ip addr add 192.168.1.100/24 dev bond0
Verify configuration:

ip link show bond0
cat /proc/net/bonding/bond0
Expected Output:
You should see bond0 interface with both slaves listed and the active-backup mode configured.

Subtask 2.2: Configure Bonding Using nmcli

Create bond connection:

sudo nmcli con add type bond ifname bond0 mode active-backup
Add slave interfaces:

sudo nmcli con add type bond-slave ifname eth0 master bond0
sudo nmcli con add type bond-slave ifname eth1 master bond0
Bring up connections:

sudo nmcli con up bond-slave-eth0
sudo nmcli con up bond-slave-eth1
sudo nmcli con up bond0
Verify:

nmcli con show
nmcli device status
Troubleshooting Tip:
If connections fail, check journal logs:

journalctl -xe
Task 3: Create Startup Script for Bonding

Subtask 3.1: Create Systemd Service

Create script /usr/local/bin/setup-bonding.sh:

#!/bin/bash
ip link add bond0 type bond mode active-backup
ip link set eth0 master bond0
ip link set eth1 master bond0
ip link set bond0 up
ip addr add 192.168.1.100/24 dev bond0
Make it executable:

sudo chmod +x /usr/local/bin/setup-bonding.sh
Create systemd service /etc/systemd/system/bonding.service:

[Unit]
Description=Network Bonding Configuration
After=network.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/setup-bonding.sh

[Install]
WantedBy=multi-user.target
Enable and start the service:

sudo systemctl daemon-reload
sudo systemctl enable bonding.service
sudo systemctl start bonding.service
Verification:
Reboot your system and check bonding status:

systemctl status bonding.service
ip a show bond0
