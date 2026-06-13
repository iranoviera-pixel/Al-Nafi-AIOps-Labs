Lab 26: Ext4 File System Tuning

Objectives

By the end of this lab, students will be able to:

Format a disk with the Ext4 file system using mkfs.ext4.
Tune Ext4 file system parameters using tune2fs.
Write a Bash script to automate Ext4 tuning for different use cases (e.g., database, general-purpose storage).
Understand key Ext4 features like journaling, reserved blocks, and mount options.
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge (e.g., ls, cd, sudo).
A Linux-based machine (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
A disk or partition to format (e.g., /dev/sdb1). Note: Use a test machine to avoid data loss.
Root/sudo access (required for disk operations).
Task 1: Format a Disk with Ext4

Step 1: Identify the Target Disk

List available disks:

lsblk
Expected Output: A list of disks (e.g., sda, sdb). Identify an unused disk (e.g., /dev/sdb).
Verify the disk is unmounted:

sudo umount /dev/sdb1
Step 2: Format as Ext4

Format the disk with default settings:

sudo mkfs.ext4 /dev/sdb1
Expected Output: Confirmation of filesystem creation and block allocation.
(Optional) Specify a label:

sudo mkfs.ext4 -L "mydata" /dev/sdb1
Task 2: Tune Ext4 with tune2fs

Step 1: View Current Settings

Check filesystem details:
sudo tune2fs -l /dev/sdb1
Key Output: Block size, Reserved blocks, Mount count, Check interval.
Step 2: Optimize Reserved Blocks

Reduce reserved blocks (default: 5%) for non-root filesystems:
sudo tune2fs -m 1 /dev/sdb1
Why: Frees space for user data on large disks.
Step 3: Disable Time-Based Checks

Disable forced filesystem checks after a set time:
sudo tune2fs -i 0 /dev/sdb1
Why: Prevents unnecessary checks if the system is rebooted infrequently.
Step 4: Enable Journaling (if disabled)

Verify journaling status:
sudo dumpe2fs /dev/sdb1 | grep has_journal
Enable journaling (if needed):
sudo tune2fs -O has_journal /dev/sdb1
Task 3: Script for Automated Tuning

Step 1: Create a Bash Script

Open a new file:
nano tune_ext4.sh
Paste the following script (customize as needed):
#!/bin/bash
# Usage: sudo ./tune_ext4.sh /dev/sdX [use_case]
# Use cases: "database", "general", "multimedia"

DEVICE=$1
USE_CASE=$2

# Common settings
tune2fs -m 1 $DEVICE       # Reduce reserved blocks
tune2fs -i 0 $DEVICE       # Disable time-based checks

# Use-case specific tuning
case $USE_CASE in
  "database")
    tune2fs -o journal_data_writeback $DEVICE  # Faster writes
    tune2fs -O dir_index $DEVICE               # Faster directory lookups
    ;;
  "multimedia")
    tune2fs -O huge_file $DEVICE               # Optimize for large files
    ;;
  *)
    echo "Using general-purpose settings."
    ;;
esac

echo "Tuning complete for $DEVICE ($USE_CASE)."
Step 2: Make the Script Executable

chmod +x tune_ext4.sh
Step 3: Run the Script

sudo ./tune_ext4.sh /dev/sdb1 database
Expected Output: Confirmation of applied settings.
Troubleshooting Tips

"Device busy" error: Ensure the disk is unmounted (umount /dev/sdb1).
Permission denied: Use sudo for all disk operations.
Invalid filesystem: Verify the disk is formatted as Ext4 (lsblk -f).
