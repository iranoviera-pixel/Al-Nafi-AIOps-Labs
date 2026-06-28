Lab 83: Virtual Network Configuration in KVM

Objectives

By the end of this lab, students will be able to:

Understand virtual networking concepts in KVM (Kernel-based Virtual Machine).
Create and manage virtual networks using virsh.
Configure NAT (Network Address Translation) and bridged networking for VMs.
Automate virtual network creation using a Bash script.
Prerequisites

Before starting, ensure you have:

A Linux-based system with KVM installed (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with Linux command-line operations.
virsh and libvirt packages installed (included in Al Nafi’s lab environment).
Sudo/root privileges (provided in the lab environment).
Task 1: Create a Virtual Network Using virsh

Step 1: List Existing Virtual Networks

Open a terminal.
Run:
virsh net-list --all
Expected Output: A list of existing networks (default may include default NAT network).
Step 2: Create an XML Configuration File

Create a file named lab83-nat.xml:
nano lab83-nat.xml
Paste the following NAT configuration:
<network>
  <name>lab83-nat</name>
  <forward mode='nat'/>
  <bridge name='virbr-lab83' stp='on' delay='0'/>
  <ip address='192.168.83.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='192.168.83.100' end='192.168.83.200'/>
    </dhcp>
  </ip>
</network>
Explanation:
forward mode='nat': Enables NAT for internet access.
bridge name='virbr-lab83': Creates a virtual bridge.
DHCP range assigns IPs to VMs automatically.
Step 3: Define and Start the Network

Define the network:
virsh net-define lab83-nat.xml
Start the network:
virsh net-start lab83-nat
Verify:
virsh net-list
Expected Outcome: lab83-nat appears in the list with "active" status.
Task 2: Configure NAT and Bridged Networking

Step 1: Verify Host Network Interfaces

Run:
ip a
Note: Identify the physical interface (e.g., eth0 or ens3).
Step 2: Create a Bridged Network

Create a bridge named br0:
sudo nmcli con add type bridge ifname br0
Add the physical interface to the bridge:
sudo nmcli con add type bridge-slave ifname eth0 master br0
Restart networking:
sudo systemctl restart NetworkManager
Step 3: Attach a VM to the Bridge

Edit a VM’s configuration:
virsh edit <VM_Name>
Replace the <interface> section with:
<interface type='bridge'>
  <source bridge='br0'/>
  <model type='virtio'/>
</interface>
Explanation: Directly connects the VM to the physical network via br0.
Task 3: Automate Network Creation with a Script

Step 1: Write a Bash Script

Create create-vnet.sh:
nano create-vnet.sh
Paste the script:
#!/bin/bash
# Usage: ./create-vnet.sh <network_name> <bridge_name> <ip_range>
NET_NAME=$1
BRIDGE=$2
IP_RANGE=$3

cat > /tmp/${NET_NAME}.xml <<EOF
<network>
  <name>$NET_NAME</name>
  <forward mode='nat'/>
  <bridge name='$BRIDGE' stp='on' delay='0'/>
  <ip address='$IP_RANGE.1' netmask='255.255.255.0'>
    <dhcp>
      <range start='$IP_RANGE.100' end='$IP_RANGE.200'/>
    </dhcp>
  </ip>
</network>
EOF

virsh net-define /tmp/${NET_NAME}.xml
virsh net-start $NET_NAME
echo "Network $NET_NAME created and started!"
Step 2: Run the Script

Make it executable:
chmod +x create-vnet.sh
Execute (example):
./create-vnet.sh lab83-auto virbr-auto 192.168.84
Expected Outcome: A new network lab83-auto with DHCP range 192.168.84.100-200.
