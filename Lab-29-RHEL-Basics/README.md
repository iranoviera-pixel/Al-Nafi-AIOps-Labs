Lab 29: Automating Storage Management Tasks

Objectives

By the end of this lab, students will be able to:

Automate disk partitioning, file system creation, and volume management using Bash scripting.
Generate disk usage and file system reports using lsblk and fdisk.
Schedule automated storage management tasks using cron.
Understand basic storage management concepts in Linux.
Prerequisites

Before starting this lab, students should:

Have basic familiarity with Linux command line.
Understand fundamental storage concepts (disks, partitions, file systems).
Know how to edit files using nano or vim.
Note: Al Nafi provides pre-configured Linux cloud machines—click Start Lab to begin (no VM setup required).
Lab Setup

Click Start Lab to launch your Linux cloud machine.
Open the terminal (Ctrl+Alt+T or use the provided terminal interface).
Task 1: Automate Partitioning, File System Creation, and Volume Management

Subtask 1.1: Create a Bash Script

We’ll write a script named automate_storage.sh to:

List available disks.
Create a partition.
Format the partition.
Mount it to a directory.
Steps:

Open a text editor:

nano automate_storage.sh
Paste the following script (explanation included as comments):

#!/bin/bash

# Display available disks
echo "Available disks:"
lsblk

# Prompt user to select a disk (e.g., /dev/sdb)
read -p "Enter the disk to partition (e.g., /dev/sdb): " disk

# Create a new partition
echo "Creating a new partition..."
sudo fdisk $disk <<EOF
n
p
1

w
EOF

# Format the partition (ext4 filesystem)
echo "Formatting the partition as ext4..."
sudo mkfs.ext4 "${disk}1"

# Create a mount point and mount the partition
sudo mkdir -p /mnt/mydisk
sudo mount "${disk}1" /mnt/mydisk

# Verify the mount
echo "Partition mounted at /mnt/mydisk:"
df -h /mnt/mydisk
Save the file (Ctrl+O, then Enter) and exit (Ctrl+X).

Subtask 1.2: Make the Script Executable

Run:

chmod +x automate_storage.sh
Subtask 1.3: Run the Script

Execute the script:

sudo ./automate_storage.sh
Expected Output:

The script will list disks, create a partition, format it, and mount it to /mnt/mydisk.
Verify with lsblk and df -h.
Troubleshooting:

If the disk is busy, unmount it first: sudo umount /dev/sdb1.
If fdisk fails, ensure the disk exists (lsblk).
Task 2: Generate Disk Usage and File System Reports

Subtask 2.1: Create a Report Script

Create disk_report.sh:

nano disk_report.sh
Paste:

#!/bin/bash

# Generate a disk report
echo "Disk Usage and File Systems Report" > disk_report.txt
echo "Generated on: $(date)" >> disk_report.txt
echo "=================================" >> disk_report.txt

# List block devices
echo "Block Devices:" >> disk_report.txt
lsblk >> disk_report.txt

# List file systems
echo -e "\nFile Systems:" >> disk_report.txt
df -Th >> disk_report.txt

echo "Report saved to disk_report.txt"
Subtask 2.2: Run the Report Script

Make it executable and run:

chmod +x disk_report.sh
./disk_report.sh
cat disk_report.txt  # View the report
Expected Output:

A file disk_report.txt with disk and file system details.
Task 3: Schedule the Script with Cron

Subtask 3.1: Schedule Daily Reports

Edit the cron table:

crontab -e
Add this line to run disk_report.sh daily at 6 AM:

0 6 * * * /path/to/disk_report.sh
Note: Replace /path/to/ with the actual path to your script.

Subtask 3.2: Verify Cron Job

List scheduled jobs:

crontab -l
