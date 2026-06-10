#!/bin/bash

# Set variables
GATEWAY_IP="192.168.64.1"
INTERFACE="enp0s1"

# Add default gateway
echo "Configuring default gateway..."
sudo ip route add default via $GATEWAY_IP dev $INTERFACE

# Verify gateway
echo "Verifying gateway..."
ip route show | grep "default"

# Test connectivity
echo "Testing connectivity to gateway..."
ping -c 4 $GATEWAY_IP

echo "Testing internet access..."
ping -c 4 google.com


