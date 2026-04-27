#!/bin/bash

# List all unmounted partitions
UNMOUNTED=$(lsblk -lno NAME,MOUNTPOINT | awk '$2=="" {print $1}')

if [ -z "$UNMOUNTED" ]; then
    echo "No unmounted partitions found."
    exit 0
fi

echo "Unmounted partitions:"
echo "$UNMOUNTED"

# Mount each unmounted partition
for PARTITION in $UNMOUNTED; do
    MOUNT_POINT="/mnt/$PARTITION"
    sudo mkdir -p "$MOUNT_POINT"
    sudo mount "/dev/$PARTITION" "$MOUNT_POINT"
    echo "Mounted /dev/$PARTITION at $MOUNT_POINT"
done


