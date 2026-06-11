Network Bonding and Bridging

Objectives

By the end of this lab, students will be able to:

Understand the concepts of network bonding (link aggregation) and bridging.
Configure network bonding using nmcli for high availability.
Set up a network bridge using brctl or nmcli to connect multiple network segments.
Write a basic script to automate bonding and bridging configurations.
Prerequisites

Before starting this lab, ensure you have:

A Linux-based machine (provided by Al Nafi's cloud lab—click Start Lab to begin).
Basic familiarity with Linux command-line interface (CLI).
Two or more network interfaces (physical or virtual) for bonding (simulated in the cloud lab).
Root or sudo privileges to configure network settings.
Task 1: Configure Network Bonding

Network bonding combines multiple network interfaces into a single logical interface for redundancy or increased bandwidth.

Subtask 1.1: Check Available Interfaces

Open a terminal.
Run the following command to list network interfaces:
ip link show
Outcome: You should see at least two interfaces (e.g., eth0, eth1).
Subtask 1.2: Create a Bonded Interface Using nmcli

Create a bond interface named bond0 with balance-rr (round-robin) mode:
sudo nmcli connection add type bond ifname bond0 mode balance-rr
Add slave interfaces (e.g., eth0 and eth1) to the bond:
sudo nmcli connection add type bond-slave ifname eth0 master bond0
sudo nmcli connection add type bond-slave ifname eth1 master bond0
Activate the bond:
sudo nmcli connection up bond0
Verify the bond status:
cat /proc/net/bonding/bond0
Expected Outcome: Output shows active slaves and bonding mode.
Troubleshooting Tips

If interfaces fail to bond, ensure they are not already in use (check with ip link show).
Restart the NetworkManager service if changes don’t apply:
sudo systemctl restart NetworkManager
Task 2: Set Up a Network Bridge

A network bridge connects multiple network segments, allowing them to communicate as a single network.

Subtask 2.1: Install Bridge Utilities (if using brctl)

Install the bridge-utils package:
sudo apt-get install bridge-utils  # Debian/Ubuntu
sudo yum install bridge-utils     # RHEL/CentOS
Subtask 2.2: Create a Bridge Using nmcli

Create a bridge named br0:
sudo nmcli connection add type bridge ifname br0
Add an interface (e.g., eth2) to the bridge:
sudo nmcli connection add type bridge-slave ifname eth2 master br0
Bring the bridge online:
sudo nmcli connection up br0
Verify the bridge:
ip link show br0
Expected Outcome: br0 appears with eth2 as a slave.
Task 3: Script for Bonding and Bridging

Automate the configuration with a Bash script.

Subtask 3.1: Write the Script

Create a file named network-setup.sh:
#!/bin/bash
# Configure bonding
sudo nmcli connection add type bond ifname bond0 mode active-backup
sudo nmcli connection add type bond-slave ifname eth0 master bond0
sudo nmcli connection add type bond-slave ifname eth1 master bond0
sudo nmcli connection up bond0

# Configure bridging
sudo nmcli connection add type bridge ifname br0
sudo nmcli connection add type bridge-slave ifname eth2 master br0
sudo nmcli connection up br0

echo "Network bonding (bond0) and bridge (br0) configured!"
Make the script executable:
chmod +x network-setup.sh
Run the script:
sudo ./network-setup.sh
Subtask 3.2: Validate the Configuration

Check bonding:
cat /proc/net/bonding/bond0
Check bridging:
bridge link show
