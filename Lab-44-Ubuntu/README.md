Lab 44: Mounting File Systems

Objectives

By the end of this lab, you will be able to:

Understand the concept of mounting file systems in Linux
Use the mount command to attach file systems
Verify mounted file systems using df -h
Automate mounting and unmounting operations using shell scripts
Prerequisites

A Linux system (Ubuntu/CentOS recommended)
Basic familiarity with Linux command line
Root or sudo privileges
An additional storage device or partition (physical or virtual) for practice
Lab Setup

Ensure your Linux system is up to date:

sudo apt update && sudo apt upgrade -y  # For Debian/Ubuntu
sudo yum update -y                     # For CentOS/RHEL
Create a practice directory:

mkdir ~/mount_lab
cd ~/mount_lab
Task 1: Mounting a File System

Subtask 1.1: Identify Available Devices

List all block devices:

lsblk
Expected Output: Shows all storage devices and partitions
Key Concept: lsblk displays block devices in a tree format
Identify an unused partition or create one:

sudo fdisk -l
Troubleshooting: If no extra partition exists, create one using fdisk (advanced)
Subtask 1.2: Create Mount Point

Create a directory to serve as mount point:
sudo mkdir /mnt/mylab
Subtask 1.3: Mount the File System

Mount the identified partition (replace /dev/sdb1 with your actual device):

sudo mount /dev/sdb1 /mnt/mylab
Key Concept: The mount command attaches a filesystem to the directory tree
Verify ownership:

ls -ld /mnt/mylab
Task 2: Verify Mounted File System

Subtask 2.1: Using df Command

Check mounted filesystems:

df -h
Expected Output: Shows /mnt/mylab in the list with available space
Key Concept: -h flag shows human-readable sizes
Get detailed filesystem info:

mount | grep mylab
Subtask 2.2: Test File Operations

Create a test file:
sudo touch /mnt/mylab/testfile.txt
ls /mnt/mylab
Task 3: Automation with Scripts

Subtask 3.1: Create Mount Script

Create mount_fs.sh:

#!/bin/bash
# Script to mount filesystem

DEVICE="/dev/sdb1"
MOUNT_POINT="/mnt/mylab"

if [ ! -d "$MOUNT_POINT" ]; then
    sudo mkdir -p "$MOUNT_POINT"
fi

sudo mount "$DEVICE" "$MOUNT_POINT" && echo "Successfully mounted $DEVICE to $MOUNT_POINT"
Make it executable:

chmod +x mount_fs.sh
Subtask 3.2: Create Unmount Script

Create unmount_fs.sh:

#!/bin/bash
# Script to unmount filesystem

MOUNT_POINT="/mnt/mylab"

sudo umount "$MOUNT_POINT" && echo "Successfully unmounted $MOUNT_POINT"
Make it executable:

chmod +x unmount_fs.sh
Subtask 3.3: Test the Scripts

Run the unmount script:

./unmount_fs.sh
Verify unmount:

df -h | grep mylab
Run mount script:

./mount_fs.sh


