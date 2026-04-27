#!/bin/bash

# Define disk and partition (KOREKSI DI SINI)
DISK="/dev/nvme1n1"
PARTITION="${DISK}p1"

# Create partition non-interactively
echo -e "n\np\n1\n\n+10G\nw" | sudo fdisk $DISK

# Format the partition
sudo mkfs.ext4 $PARTITION

echo "Partition created and formatted: $PARTITION"

MOUNT_POINT="/mnt/mydata"

# Create mount point if it doesn't exist
sudo mkdir -p $MOUNT_POINT

# Mount the partition
sudo mount $PARTITION $MOUNT_POINT

# Verify mount
df -h | grep $MOUNT_POINT


