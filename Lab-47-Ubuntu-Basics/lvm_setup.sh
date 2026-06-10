#!/bin/bash

# Define variables
PV="/dev/loop18"
VG="vg_data"
LV="lv_storage"
SIZE="10G"
MOUNT_POINT="/mnt/lvm_storage"

# Create PV
pvcreate $PV || { echo "PV creation failed"; exit 1; }

# Create VG
vgcreate $VG $PV || { echo "VG creation failed"; exit 1; }

# Create LV
lvcreate -L $SIZE -n $LV $VG || { echo "LV creation failed"; exit 1; }

# Format and mount
mkfs.ext4 /dev/$VG/$LV || { echo "Formatting failed"; exit 1; }
mkdir -p $MOUNT_POINT
mount /dev/$VG/$LV $MOUNT_POINT || { echo "Mount failed"; exit 1; }

echo "LVM setup completed successfully!"
