Lab 78: Setting Up Failover Network

Objectives

By the end of this lab, you will be able to:

Configure a secondary network interface for failover using ifenslave or nmcli.
Implement automatic network switching during primary interface failure.
Develop a monitoring script to manage failover events between interfaces.
Prerequisites

A Linux system (Ubuntu/CentOS/RHEL) with two active network interfaces (e.g., eth0 and eth1).
Root or sudo privileges.
Basic familiarity with Linux networking commands (ip, ifconfig, nmcli).
ifenslave package (for bonding) or NetworkManager (for nmcli).
Task 1: Set Up a Secondary Network Interface for Failover

Subtask 1.1: Install Required Tools

For bonding (ifenslave):

sudo apt update && sudo apt install ifenslave -y  # Debian/Ubuntu
sudo yum install ifenslave -y                     # CentOS/RHEL
For NetworkManager (nmcli):

sudo apt install network-manager -y  # Debian/Ubuntu
sudo yum install NetworkManager -y   # CentOS/RHEL
Expected Outcome: Packages installed without errors.

Subtask 1.2: Configure Bonding (ifenslave)

Load the bonding kernel module:
sudo modprobe bonding
Create a bond interface (bond0) configuration:
sudo nano /etc/network/interfaces  # Debian/Ubuntu
Add:
auto bond0
iface bond0 inet dhcp
    bond-mode active-backup
    bond-miimon 100
    bond-primary eth0
    bond-slaves eth0 eth1
Restart networking:
sudo systemctl restart networking  # Debian/Ubuntu
sudo systemctl restart network     # CentOS/RHEL
Expected Outcome: bond0 interface appears in ip a with eth0 and eth1 as slaves.

Subtask 1.3: Configure Failover with nmcli

Create a connection profile for bonding:
sudo nmcli con add type bond ifname bond0 mode active-backup
Add slaves:
sudo nmcli con add type bond-slave ifname eth0 master bond0
sudo nmcli con add type bond-slave ifname eth1 master bond0
Activate the bond:
sudo nmcli con up bond0
Expected Outcome: nmcli con show lists bond0 with eth0 and eth1 as slaves.

Task 2: Configure Automatic Switching on Failure

Subtask 2.1: Test Failover Manually

Disable eth0 to trigger failover:
sudo ip link set eth0 down
Verify traffic routes via eth1:
ip route show
Expected Outcome: Default route switches to eth1.

Subtask 2.2: Automate Monitoring (Script)

Create a script /usr/local/bin/failover-monitor.sh:

#!/bin/bash
INTERFACE="eth0"
BACKUP_INTERFACE="eth1"
PING_TARGET="8.8.8.8"

while true; do
    if ! ping -c 1 -I $INTERFACE $PING_TARGET &> /dev/null; then
        echo "$(date): $INTERFACE failed. Switching to $BACKUP_INTERFACE."
        ip route replace default via $(ip -4 addr show $BACKUP_INTERFACE | grep inet | awk '{print $2}' | cut -d'/' -f1)
    fi
    sleep 10
done
Make it executable:

sudo chmod +x /usr/local/bin/failover-monitor.sh
Expected Outcome: Script logs failover events to /var/log/syslog.

Task 3: Manage Failover Events

Subtask 3.1: Run Script as Service

Create a systemd service:
sudo nano /etc/systemd/system/failover-monitor.service
Add:
[Unit]
Description=Failover Network Monitor

[Service]
ExecStart=/usr/local/bin/failover-monitor.sh
Restart=always

[Install]
WantedBy=multi-user.target
Start the service:
sudo systemctl daemon-reload
sudo systemctl start failover-monitor
sudo systemctl enable failover-monitor
Expected Outcome: Service runs persistently and survives reboots.

