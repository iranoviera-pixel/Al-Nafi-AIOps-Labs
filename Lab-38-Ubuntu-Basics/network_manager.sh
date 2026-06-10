#!/bin/bash
INTERFACE="enp0s1"

# Check if interface exists
if ip link show $INTERFACE > /dev/null 2>&1; then
    echo "Interface $INTERFACE found."
    
    # Check current status
    if ip link show $INTERFACE | grep -q "state UP"; then
        echo "Bringing $INTERFACE down..."
        sudo ifdown $INTERFACE
    else
        echo "Bringing $INTERFACE up..."
        sudo ifup $INTERFACE
    fi
else
    echo "Error: Interface $INTERFACE not found."
fi
