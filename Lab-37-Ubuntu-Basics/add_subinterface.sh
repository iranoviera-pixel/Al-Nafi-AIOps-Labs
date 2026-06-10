#!/bin/bash

# Define primary interface and sub-interface details
PRIMARY_IF="enp0s1"
SUBNET="192.168.64"
START_IP=102
NUM_INTERFACES=3

# Loop to create sub-interfaces
for i in $(seq 1 $NUM_INTERFACES); do
    SUB_IF="${PRIMARY_IF}:${i}"
    IP="${SUBNET}.${START_IP}"

    # Add sub-interface
    sudo ip addr add ${IP}/24 dev ${PRIMARY_IF} label ${SUB_IF}

    # Verify
    echo "Created ${SUB_IF} with IP ${IP}"
    ip addr show ${SUB_IF} | grep inet

    START_IP=$((START_IP + 1))
done


