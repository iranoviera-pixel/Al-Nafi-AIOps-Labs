#!/bin/bash
INTERFACE="enp0s1"
IP="192.168.1.100"
GATEWAY="192.168.1.1"
DNS="8.8.8.8"

echo "Setting static IP $IP on $INTERFACE..."
cat > /etc/netplan/01-netcfg.yaml <<EOF
network:
  version: 2
  renderer: networkd
  ethernets:
    $INTERFACE:
      dhcp4: no
      addresses: [$IP/24]
      gateway4: $GATEWAY
      nameservers:
        addresses: [$DNS]
EOF

netplan apply
echo "Configuration applied. Verify with 'ip a'"
