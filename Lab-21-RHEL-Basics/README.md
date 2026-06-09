Lab 21: Disk Partitioning Using fdisk and parted

Objectives

By the end of this lab, students will be able to:

Use fdisk to create, delete, and modify disk partitions.
Use parted to manage partition tables and advanced disk operations.
Write a Bash script to automate partition creation for different disk sizes and file systems.
Prerequisites

Before starting, ensure you have:

A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with Linux command-line operations.
A non-root user with sudo privileges (provided in Al Nafi’s environment).
A secondary disk attached to the VM (e.g., /dev/sdb). Note: Al Nafi labs include this by default.
Task 1: Using fdisk to Manage Partitions

Step 1: List Available Disks

Open a terminal.
Run the following command to list disks:
lsblk
Expected Output: A list of disks (e.g., sda, sdb) and their partitions.
Step 2: Launch fdisk

Start fdisk on the target disk (e.g., /dev/sdb):
sudo fdisk /dev/sdb
Troubleshooting: If fdisk is not installed, run sudo apt install fdisk (Debian/Ubuntu) or sudo yum install util-linux (RHEL/CentOS).
Step 3: Create a New Partition

Inside fdisk:
Press n to create a new partition.
Select p for primary or e for extended.
Accept default values for partition number and first sector.
Specify size (e.g., +2G for 2GB).
Press w to write changes.
Command (m for help): n
Partition type: p
Partition number: 1
First sector: (default)
Last sector: +2G
Command (m for help): w
Expected Outcome: A new partition /dev/sdb1 is created.
Step 4: Delete a Partition

Reopen fdisk:
sudo fdisk /dev/sdb
Press d to delete, select the partition number, and press w to save.
Task 2: Using parted for Advanced Partitioning

Step 1: Install parted (if missing)

sudo apt install parted  # Debian/Ubuntu
sudo yum install parted  # RHEL/CentOS
Step 2: Create a GPT Partition Table

Launch parted:
sudo parted /dev/sdb
Create a GPT table:
(parted) mklabel gpt
Add a 3GB partition:
(parted) mkpart primary ext4 1MiB 3GiB
Exit with quit.
Task 3: Automate Partitioning with a Script

Step 1: Write a Bash Script

Create a script auto_partition.sh:

#!/bin/bash
DISK="/dev/sdb"
PARTITION_SIZE="2G"
FS_TYPE="ext4"

# Create partition
echo "Creating partition..."
sudo parted $DISK mklabel gpt
sudo parted $DISK mkpart primary $FS_TYPE 0% $PARTITION_SIZE

# Format and mount
sudo mkfs.$FS_TYPE ${DISK}1
sudo mkdir /mnt/data
sudo mount ${DISK}1 /mnt/data
echo "Partition created and mounted at /mnt/data"
Step 2: Make the Script Executable

chmod +x auto_partition.sh
Step 3: Run the Script

sudo ./auto_partition.sh
Expected Outcome: A 2GB /dev/sdb1 partition formatted as ext4 and mounted at /mnt/data.

