Configuring IPv4 and IPv6 Addressing

Objectives

By the end of this lab, students will be able to:

Configure static IPv4 and IPv6 addresses using nmcli.
Set up a network interface with dual-stack (IPv4 + IPv6) addressing.
Automate IP address assignment using a Bash script.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line.
A Linux-based machine (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
nmcli (NetworkManager command-line tool) installed (default on most Linux distributions).
Task 1: Configure Static IPv4 and IPv6 Addresses Using nmcli

Step 1: List Available Network Interfaces

Run the following command to identify the interface you want to configure:

nmcli device status
Expected Output:
A table showing interfaces (e.g., eth0, ens33) and their status.

Step 2: Configure Static IPv4 Address

Replace eth0 with your interface name and set the IPv4 address (192.168.1.100/24) and gateway (192.168.1.1):

sudo nmcli connection modify eth0 ipv4.addresses 192.168.1.100/24
sudo nmcli connection modify eth0 ipv4.gateway 192.168.1.1
sudo nmcli connection modify eth0 ipv4.method manual
Explanation:

ipv4.method manual: Sets static IP (default is auto for DHCP).
Step 3: Configure Static IPv6 Address

Set the IPv6 address (2001:db8::100/64) and gateway (2001:db8::1):

sudo nmcli connection modify eth0 ipv6.addresses 2001:db8::100/64
sudo nmcli connection modify eth0 ipv6.gateway 2001:db8::1
sudo nmcli connection modify eth0 ipv6.method manual
Step 4: Apply Changes

Restart the connection:

sudo nmcli connection down eth0 && sudo nmcli connection up eth0
Verification:
Run ip a show eth0 to confirm the IPv4/IPv6 addresses appear.

Task 2: Set Up Dual-Stack (IPv4 + IPv6) Interface

Step 1: Edit Connection Profile

Use nmcli to enable both IPv4 and IPv6:

sudo nmcli connection modify eth0 ipv4.method manual ipv6.method manual
Step 2: Assign Both Addresses

Combine IPv4 and IPv6 settings from Task 1 into one command:

sudo nmcli connection modify eth0 \
  ipv4.addresses 192.168.1.100/24 \
  ipv4.gateway 192.168.1.1 \
  ipv6.addresses 2001:db8::100/64 \
  ipv6.gateway 2001:db8::1
Step 3: Restart Interface

sudo nmcli connection reload eth0
sudo nmcli connection up eth0
Expected Outcome:
ping6 2001:db8::1 and ping 192.168.1.1 should succeed (if gateways are reachable).

Task 3: Automate IP Assignment with a Bash Script

Step 1: Create a Script

Open a file named set_dual_stack.sh:

#!/bin/bash
INTERFACE="eth0"
IPv4_ADDR="192.168.1.100/24"
IPv4_GW="192.168.1.1"
IPv6_ADDR="2001:db8::100/64"
IPv6_GW="2001:db8::1"

nmcli connection modify $INTERFACE \
  ipv4.addresses $IPv4_ADDR \
  ipv4.gateway $IPv4_GW \
  ipv4.method manual \
  ipv6.addresses $IPv6_ADDR \
  ipv6.gateway $IPv6_GW \
  ipv6.method manual

nmcli connection down $INTERFACE && nmcli connection up $INTERFACE
Step 2: Make the Script Executable

chmod +x set_dual_stack.sh
Step 3: Run the Script

sudo ./set_dual_stack.sh
Troubleshooting:
If the script fails, check:

Correct interface name (ip link show).
Syntax errors using bash -n set_dual_stack.sh.
