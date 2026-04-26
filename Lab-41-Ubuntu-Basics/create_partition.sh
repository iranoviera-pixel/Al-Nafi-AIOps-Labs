#!/bin/bash

# Define variables
DISK="/dev/nvme1n1"
PARTITION_SIZE="+5G"
PARTITION_TYPE="p"

# Create partition non-interactively
echo -e "n\n${PARTITION_TYPE}\n\n\n${PARTITION_SIZE}\nw" | sudo fdisk $DISK

# Verify the partition
echo "Partition created:"
lsblk $DISK
