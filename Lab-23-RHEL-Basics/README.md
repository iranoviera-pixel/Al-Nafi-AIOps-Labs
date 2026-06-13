Lab 23: Creating and Managing LVM Snapshots

Objectives

By the end of this lab, you will be able to:

Understand the purpose and benefits of LVM snapshots
Create and manage LVM snapshots using lvcreate
Mount and test LVM snapshots
Automate snapshot creation and mounting with a bash script
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge (e.g., ls, cd, sudo)
A Linux-based machine (Al Nafi provides pre-configured cloud machines—click Start Lab to begin)
LVM (Logical Volume Manager) installed (included in most Linux distributions)
A logical volume (LV) to snapshot (we’ll create one if needed)
Task 1: Create a Snapshot of a Logical Volume

Step 1: Verify Available Logical Volumes

Open a terminal.
Run the following command to list logical volumes:
sudo lvs
Expected Output: A table showing existing LVs (e.g., lv_root, lv_home). If none exist, proceed to Step 2.
Step 2: Create a Logical Volume (If Needed)

List physical volumes to identify free space:
sudo pvs
Create a 1GB LV named lab_lv in the vg00 volume group (adjust names as needed):
sudo lvcreate -L 1G -n lab_lv vg00
Format the LV with ext4:
sudo mkfs.ext4 /dev/vg00/lab_lv
Step 3: Create a Snapshot

Create a 500MB snapshot named lab_snapshot of lab_lv:
sudo lvcreate -s -L 500M -n lab_snapshot /dev/vg00/lab_lv
Flags Explained:
-s: Creates a snapshot.
-L: Specifies size (ensure it’s large enough to hold changes).
Verify the snapshot:
sudo lvs
Expected Output: lab_snapshot appears under the LV list.
Task 2: Mount and Test the Snapshot

Step 1: Mount the Snapshot

Create a mount point:
sudo mkdir /mnt/lab_snapshot
Mount the snapshot:
sudo mount /dev/vg00/lab_snapshot /mnt/lab_snapshot
Step 2: Test the Snapshot

Add a test file to the original LV:
sudo touch /mnt/lab_lv/test_file.txt
Verify the file exists in the snapshot:
ls /mnt/lab_snapshot
Expected Outcome: test_file.txt appears in both locations.
Step 3: Unmount and Remove (Optional)

Unmount the snapshot:
sudo umount /mnt/lab_snapshot
Remove the snapshot (if no longer needed):
sudo lvremove /dev/vg00/lab_snapshot
Task 3: Automate Snapshot Creation with a Script

Step 1: Create a Bash Script

Open a text editor (e.g., nano):
nano lvm_snapshot.sh
Paste the following script:
#!/bin/bash
# Script to create and mount an LVM snapshot

LV_PATH="/dev/vg00/lab_lv"
SNAPSHOT_NAME="auto_snapshot_$(date +%Y%m%d)"
MOUNT_DIR="/mnt/auto_snapshot"

# Create snapshot
sudo lvcreate -s -L 500M -n "$SNAPSHOT_NAME" "$LV_PATH"

# Create mount directory
sudo mkdir -p "$MOUNT_DIR"

# Mount snapshot
sudo mount "/dev/vg00/$SNAPSHOT_NAME" "$MOUNT_DIR"

echo "Snapshot created and mounted at $MOUNT_DIR"
Step 2: Run the Script

Make the script executable:
chmod +x lvm_snapshot.sh
Execute it:
./lvm_snapshot.sh
Expected Outcome: Confirmation message and a mounted snapshot at /mnt/auto_snapshot.
Troubleshooting Tips

"Insufficient space for snapshot": Increase the snapshot size (-L) or reduce changes to the original LV.
Mount errors: Ensure the LV is not already mounted or corrupted (sudo fsck /dev/vg00/lab_snapshot).
