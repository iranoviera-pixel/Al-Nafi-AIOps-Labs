Lab 24: Stratis Storage Management Basics

Objectives

By the end of this lab, you will be able to:

Understand Stratis storage management and its advantages.
Install and configure Stratis on a Linux system.
Create and manage Stratis pools and volumes.
Automate Stratis pool/volume creation using a Bash script.
Prerequisites

Before starting, ensure you have:

A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with Linux command-line operations.
Administrative (root) access or sudo privileges.
Task 1: Install Stratis on the System

Step 1: Update System Packages

Ensure your system is up-to-date:

sudo dnf update -y  # For RHEL/CentOS/Fedora
sudo apt update && sudo apt upgrade -y  # For Debian/Ubuntu
Step 2: Install Stratis Packages

Install Stratis and its dependencies:

sudo dnf install stratisd stratis-cli -y  # RHEL/CentOS/Fedora
sudo apt install stratisd stratis-cli -y  # Debian/Ubuntu
Step 3: Start and Enable Stratis Service

Start the Stratis daemon and enable it to run at boot:

sudo systemctl enable --now stratisd
Verification:

sudo systemctl status stratisd
Expected Output:
The service should show as active (running).

Troubleshooting Tip:
If the service fails, check logs with journalctl -u stratisd.

Task 2: Create a Stratis Pool and Volume

Step 1: Identify Available Disks

List block devices to identify unused disks for the pool:

lsblk
Note: Use a disk without partitions (e.g., /dev/sdb).

Step 2: Create a Stratis Pool

Create a pool named lab_pool using the disk:

sudo stratis pool create lab_pool /dev/sdb
Verification:

sudo stratis pool list
Expected Output:
lab_pool should appear in the list.

Step 3: Create a Filesystem (Volume)

Create a volume named lab_volume in the pool:

sudo stratis fs create lab_pool lab_volume
Verification:

sudo stratis fs list lab_pool
Expected Output:
lab_volume should be listed under lab_pool.

Step 4: Mount the Volume

Mount the volume to /mnt/stratis_volume:

sudo mkdir -p /mnt/stratis_volume
sudo mount /stratis/lab_pool/lab_volume /mnt/stratis_volume
Verify Mount:

df -h /mnt/stratis_volume
Expected Output:
The filesystem should show mounted with available space.

Task 3: Automate Pool/Volume Creation with a Script

Step 1: Write the Script

Create a script stratis_auto.sh to automate pool/volume creation:

#!/bin/bash

# Define variables
POOL_NAME="auto_pool"
VOLUME_NAME="auto_volume"
DISK="/dev/sdc"  # Change to an unused disk
MOUNT_POINT="/mnt/auto_stratis"

# Create pool
sudo stratis pool create $POOL_NAME $DISK

# Create volume
sudo stratis fs create $POOL_NAME $VOLUME_NAME

# Mount volume
sudo mkdir -p $MOUNT_POINT
sudo mount /stratis/$POOL_NAME/$VOLUME_NAME $MOUNT_POINT

echo "Stratis pool '$POOL_NAME' and volume '$VOLUME_NAME' created and mounted at '$MOUNT_POINT'."
Step 2: Make the Script Executable

chmod +x stratis_auto.sh
Step 3: Run the Script

sudo ./stratis_auto.sh
Verification:

sudo stratis pool list
sudo stratis fs list auto_pool
df -h /mnt/auto_stratis
