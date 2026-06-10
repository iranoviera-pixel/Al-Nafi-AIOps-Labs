Lab 25: XFS File System Tuning

Objectives

By the end of this lab, students will be able to:

Format a disk with the XFS file system using mkfs.xfs.
Tune and optimize XFS file systems using tools like xfs_admin and xfs_growfs.
Write a basic script to monitor and adjust XFS performance based on system load.
Prerequisites

Before starting, ensure you have:

A Linux-based system (Al Nafi cloud machine recommended).
Basic familiarity with Linux command-line operations.
A non-root user with sudo privileges.
A secondary disk or partition for testing (automatically provided in Al Nafi labs).
Lab Setup

Note: Al Nafi provides pre-configured Linux cloud machines. Click Start Lab to begin—no additional setup is needed.

Task 1: Format a Disk with XFS

Step 1: Identify the Target Disk

List available disks using lsblk:

lsblk
Expected Output: A list of disks (e.g., sdb or vdb for a secondary disk).
Verify the disk is unmounted:

sudo umount /dev/sdX  # Replace sdX with your disk (e.g., sdb)
Step 2: Format the Disk with XFS

Use mkfs.xfs to create an XFS file system:

sudo mkfs.xfs -f /dev/sdX
Flags:
-f: Force overwrite if a file system exists.
Expected Output: Confirmation of XFS creation.
Verify the file system:

sudo blkid /dev/sdX
Expected Output: TYPE="xfs" in the output.
Task 2: Tune and Optimize XFS

Step 1: Adjust File System Parameters with xfs_admin

Enable lazy counters (reduces overhead for large file systems):

sudo xfs_admin -l /dev/sdX
Expected Output: Displays current lazy counter status.
Change the file system label:

sudo xfs_admin -L "mydata" /dev/sdX
Expected Output: No errors; verify with sudo xfs_admin -l /dev/sdX.
Step 2: Resize an XFS File System

If the disk size increases (e.g., in cloud environments), use xfs_growfs:
sudo xfs_growfs /mount/point  # Replace with your mount path
Note: Requires the file system to be mounted.
Task 3: Monitor and Tune Performance with a Script

Step 1: Create a Monitoring Script

Open a new file xfs_monitor.sh:

nano xfs_monitor.sh
Paste the following script:

#!/bin/bash
# Monitor XFS performance and adjust logbuf count under high load.

LOAD_THRESHOLD=5  # Set your desired load threshold (e.g., 5)
CURRENT_LOAD=$(cat /proc/loadavg | awk '{print $1}')

if (( $(echo "$CURRENT_LOAD > $LOAD_THRESHOLD" | bc -l) )); then
    echo "High load detected ($CURRENT_LOAD). Tuning XFS..."
    sudo xfs_admin -c "logbufs=8" /dev/sdX  # Increase log buffers
    echo "XFS tuned for high load."
else
    echo "System load normal ($CURRENT_LOAD). No tuning needed."
fi
Make the script executable:

chmod +x xfs_monitor.sh
Step 2: Test the Script

Run the script manually:
./xfs_monitor.sh
Expected Output: A message indicating the system load and whether tuning was applied.
Troubleshooting Tips

Error: "Device busy": Ensure the disk is unmounted before formatting.
Permission Denied: Use sudo for administrative commands.
Invalid Load Threshold: Adjust LOAD_THRESHOLD in the script based on your system’s CPU cores.
