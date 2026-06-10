#!/bin/bash

# Check root access
if [ "$(id -u)" -ne 0 ]; then
  echo "Run with sudo or as root."
  exit 1
fi

# List disks
echo "=== Available Disks ==="
lsblk -d | grep disk

# Get partition details
echo -e "\n=== Partition Details ==="
for disk in $(lsblk -d | grep disk | awk '{print $1}'); do
  echo "Disk: /dev/$disk"
  sudo fdisk -l /dev/$disk | grep -E "^/dev/"
done

# Check free space
echo -e "\n=== Free Space ==="
df -h --output=source,size,used,avail,pcent

