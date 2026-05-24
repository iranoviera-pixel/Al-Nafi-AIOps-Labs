Lab 76: Setting Up Teaming Network

Objectives

By the end of this lab, you will be able to:

Understand network teaming concepts in Linux.
Configure a network team using nmcli or teamd.
Set up two network interfaces for redundancy and load balancing.
Verify teaming functionality through a custom script.
Prerequisites

A Linux system (e.g., CentOS 8/9, RHEL 8/9, or Fedora) with root/sudo access.
Two physical or virtual network interfaces (e.g., eth0, eth1).
Basic familiarity with Linux command line and networking.
Task 1: Set Up a Network Team Using nmcli or teamd

Subtask 1.1: Install Required Packages

Ensure the teamd and NetworkManager packages are installed:

sudo dnf install teamd NetworkManager -y  # For RHEL/CentOS/Fedora
Subtask 1.2: Create a Network Team

Option A: Using nmcli (Recommended)

sudo nmcli connection add type team con-name team0 ifname team0 \
    config '{"runner": {"name": "activebackup"}}'
Explanation: Creates a team interface team0 with activebackup mode (failover).
Option B: Using teamd (Legacy)

Create a config file /etc/teamd/team0.conf:

{
  "device": "team0",
  "runner": {"name": "activebackup"},
  "link_watch": {"name": "ethtool"}
}
Then start the team:

sudo teamd -f /etc/teamd/team0.conf -d
Expected Outcome:

A team interface team0 is created but has no slaves yet.
Task 2: Configure Two Network Interfaces for Teaming

Subtask 2.1: Add Interfaces to the Team

Using nmcli:

sudo nmcli connection add type team-slave con-name team0-port1 ifname eth0 master team0
sudo nmcli connection add type team-slave con-name team0-port2 ifname eth1 master team0
Using teamd:

sudo teamdctl team0 port add eth0
sudo teamdctl team0 port add eth1
Subtask 2.2: Assign IP Address and Activate

sudo nmcli connection modify team0 ipv4.addresses 192.168.1.100/24
sudo nmcli connection modify team0 ipv4.gateway 192.168.1.1
sudo nmcli connection modify team0 ipv4.method manual
sudo nmcli connection up team0
Expected Outcome:

eth0 and eth1 are now slaves of team0.
team0 is active with the assigned IP.
Task 3: Verify Teaming with a Failover Script

Subtask 3.1: Create a Script to Check Team Status

Save as check_team.sh:

#!/bin/bash
echo "Team Status:"
sudo teamdctl team0 state
echo -e "\nInterface Stats:"
ip link show eth0
ip link show eth1
Make it executable:

chmod +x check_team.sh
Subtask 3.2: Test Failover

Simulate failure on eth0:
sudo ip link set eth0 down
Run the script:
./check_team.sh
Expected Output: eth0 shows DOWN, traffic fails over to eth1.
Troubleshooting Tips:

If teaming fails, check logs: journalctl -xe.
Ensure no other service (e.g., NetworkManager) conflicts with teamd.

