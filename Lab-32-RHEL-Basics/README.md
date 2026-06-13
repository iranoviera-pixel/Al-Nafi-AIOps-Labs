Lab 31: Using NetworkManager CLI and nm-tui

Objectives

By the end of this lab, you will be able to:

Install and configure network interfaces using nmcli (NetworkManager Command Line Interface).
Use nm-tui (NetworkManager Text User Interface) for interactive network configuration.
Automate network configuration by writing a basic script using nmcli.
Prerequisites

Before starting, ensure you have:

A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with the Linux terminal.
Sudo/root privileges to install packages and modify network settings.
Task 1: Install and Configure Network Interfaces Using nmcli

Step 1: Verify NetworkManager Installation

Open the terminal.
Check if NetworkManager is installed:
nmcli --version
Expected Output: Displays the installed version (e.g., 1.40.0).
Troubleshooting: If not installed, run:
sudo apt install network-manager  # Debian/Ubuntu
sudo yum install NetworkManager   # RHEL/CentOS
Step 2: List Available Network Interfaces

Run:
nmcli device status
Expected Output: A table showing devices (e.g., eth0, wlan0) and their connection status.
Step 3: Configure a Static IP Address

Disable automatic DHCP configuration for an interface (e.g., eth0):
sudo nmcli connection modify eth0 ipv4.method manual
Assign a static IP, gateway, and DNS:
sudo nmcli connection modify eth0 ipv4.addresses 192.168.1.100/24
sudo nmcli connection modify eth0 ipv4.gateway 192.168.1.1
sudo nmcli connection modify eth0 ipv4.dns "8.8.8.8"
Restart the connection:
sudo nmcli connection down eth0 && sudo nmcli connection up eth0
Verification: Run ip addr show eth0 to confirm the new IP.
Task 2: Use nm-tui for Network Configuration

Step 1: Launch nm-tui

In the terminal, run:
sudo nmtui
A text-based UI will open.
Step 2: Edit a Connection

Select Edit a connection > Choose an interface (e.g., eth0) > Edit.
Navigate to IPv4 Configuration and select Manual.
Enter:
IP Address: 192.168.1.100/24
Gateway: 192.168.1.1
DNS: 8.8.8.8
Press OK > Back > Activate a connection to apply changes.
Step 3: Verify Changes

Exit nmtui and run:
ping -c 4 google.com
Expected Outcome: Successful ping replies confirm connectivity.
Task 3: Automate Configuration with a Script

Step 1: Create a Bash Script

Open a text editor (e.g., nano network_setup.sh).
Paste the following:
#!/bin/bash
# Configure eth0 with static IP
sudo nmcli connection modify eth0 ipv4.method manual \
    ipv4.addresses 192.168.1.100/24 \
    ipv4.gateway 192.168.1.1 \
    ipv4.dns "8.8.8.8"
sudo nmcli connection down eth0 && sudo nmcli connection up eth0
echo "Network configuration applied!"
Step 2: Make the Script Executable

Run:
chmod +x network_setup.sh
Execute the script:
./network_setup.sh
Conclusion

In this lab, you:

Learned to configure networks using both CLI (nmcli) and TUI (nmtui).
Automated network setup with a script, saving time for repetitive tasks.
Gained foundational skills for managing Linux networks, critical for system administration.
Why It Matters: NetworkManager tools simplify network management across distributions, making them essential for cloud, DevOps, and IT roles.
