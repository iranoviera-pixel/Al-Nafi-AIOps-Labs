Lab 22: Working with Logical Volume Management (LVM)

Objectives

By the end of this lab, you will be able to:

Understand the basics of Logical Volume Management (LVM).
Create and manage Physical Volumes (PVs), Volume Groups (VGs), and Logical Volumes (LVs).
Automate LVM setup using a Bash script.
Apply LVM concepts to real-world storage management scenarios.
Prerequisites

Before starting this lab, ensure you have:

Basic Linux command-line knowledge (e.g., ls, fdisk, sudo).
A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Root or sudo privileges (required for LVM commands).
Unallocated disk space (or a virtual disk to practice on).
Lab Setup

Tools Used: Open-source LVM tools (lvm2 package).
OS: Linux (Ubuntu/CentOS/RHEL).
Cloud Machine: Use Al Nafi’s provided Linux VM (no setup needed).
Task 1: Create Physical Volumes (PVs) with pvcreate

Step 1: Check Available Disks

List all disks attached to your system:

lsblk
Expected Output:
Identify unused disks (e.g., sdb, sdc).

Step 2: Create a Physical Volume

Use pvcreate to initialize a disk as a PV:

sudo pvcreate /dev/sdb
Verification:

sudo pvs
Expected Output:
Lists PVs with details like size and VG association.

Task 2: Create a Volume Group (VG) with vgcreate

Step 1: Create a VG Named my_vg

Combine PVs into a VG:

sudo vgcreate my_vg /dev/sdb
Verification:

sudo vgs
Expected Output:
Shows my_vg with total/free space.

Task 3: Create Logical Volumes (LVs) with lvcreate

Step 1: Create an LV Named my_lv

Allocate 5GB from my_vg:

sudo lvcreate -L 5G -n my_lv my_vg
Verification:

sudo lvs
Expected Output:
Displays my_lv with size and VG.

Step 2: Format and Mount the LV

Format as ext4 and mount to /mnt/mydata:

sudo mkfs.ext4 /dev/my_vg/my_lv
sudo mkdir -p /mnt/mydata
sudo mount /dev/my_vg/my_lv /mnt/mydata
Verification:

df -h /mnt/mydata
Expected Output:
Shows mounted LV with 5GB capacity.

Task 4: Automate LVM Setup with a Script

Step 1: Write a Bash Script

Create lvm_setup.sh:

#!/bin/bash
# Initialize PV, VG, and LV
pvcreate /dev/sdb
vgcreate my_vg /dev/sdb
lvcreate -L 5G -n my_lv my_vg
mkfs.ext4 /dev/my_vg/my_lv
mkdir -p /mnt/mydata
mount /dev/my_vg/my_lv /mnt/mydata
echo "LVM setup complete!"
Make it executable:

chmod +x lvm_setup.sh
sudo ./lvm_setup.sh
Step 2: Verify Automation

Check outputs of pvs, vgs, and lvs.

Troubleshooting Tips

Disk Not Found: Ensure the disk (/dev/sdb) exists via lsblk.
Permission Denied: Prefix commands with sudo.
Mount Point Busy: Unmount first (sudo umount /mnt/mydata).
