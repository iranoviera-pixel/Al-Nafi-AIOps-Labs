#!/bin/bash

# Input variables
PARTITION=$1
FS_TYPE=$2
MOUNT_POINT=$3

# Validate inputs
if [ -z "$PARTITION" ] || [ -z "$FS_TYPE" ] || [ -z "$MOUNT_POINT" ]; then
    echo "Usage: $0 <partition> <fs_type> <mount_point>"
    exit 1
fi

# Create file system
case $FS_TYPE in
    ext4)
        mkfs.ext4 $PARTITION
        ;;
    xfs)
        mkfs.xfs $PARTITION
        ;;
    *)
        echo "Unsupported file system: $FS_TYPE"
        exit 1
esac

# Create mount point and mount
mkdir -p $MOUNT_POINT
mount $PARTITION $MOUNT_POINT
echo "File system $FS_TYPE created on $PARTITION and mounted at $MOUNT_POINT"


