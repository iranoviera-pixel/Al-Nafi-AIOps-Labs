Lab 30: Configuring Networking in Linux
Description
This documentation outlines the steps taken to configure networking on an Ubuntu system. The lab covers transitioning from dynamic (DHCP) to static IP configuration using the Netplan utility.

1. Network Interface Identification
Before applying any changes, the active network interface was identified to ensure the configuration was applied to the correct hardware/virtual slot.

Command: ip a

Identified Interface: enp0s1 (Note: System previously identified this as ens5 in earlier sessions).

2. Static IP Implementation
The network configuration was manually defined by editing the Netplan YAML file located at /etc/netplan/01-netcfg.yaml.

Configuration Details:

Parameter	Value
IP Address	192.168.1.100/24
Gateway	192.168.1.1
DNS Servers	8.8.8.8, 8.8.4.4
Configuration Snippet:

YAML
network:
  version: 2
  renderer: networkd
  ethernets:
    enp0s1:
      addresses: [192.168.1.100/24]
      gateway4: 192.168.1.1
      nameservers:
        addresses: [8.8.8.8, 8.8.4.4]
3. Verification & Results
After applying the configuration with sudo netplan apply, the changes were verified to ensure the interface correctly adopted the static IP.

Verification Command:

Bash
ip a show enp0s1
Expected Output:

Plaintext
inet 192.168.1.100/24 brd 192.168.1.255 scope global noprefixroute enp0s1
4. Troubleshooting & Observations
Warning Messages: During netplan apply, warnings regarding "Permissions are too open" and "gateway4 is deprecated" were observed. These were acknowledged as non-critical for this lab environment.

Connectivity: Validated the configuration by performing a ping test to the DNS servers to ensure external connectivity was maintained.
