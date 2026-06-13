Lab 28: Configuring Quotas for Disk Usage Management

Objectives

By the end of this lab, students will be able to:

Understand the concept of disk quotas in Linux.
Enable and configure disk quotas on a file system.
Set soft and hard limits for users using edquota.
Automate quota management using a Bash script.
Prerequisites

Before starting this lab, ensure you have:

Basic familiarity with Linux command line.
A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Administrative/sudo privileges to modify system settings.
Task 1: Enable Disk Quotas on File Systems

Step 1: Check File System Support

Open a terminal.
Verify if your file system supports quotas by running:
mount | grep ' / '
Expected Output: Look for usrquota or grpquota in the options. If missing, proceed to Step 2.
Step 2: Enable Quotas Temporarily

Remount the root file system with quota support:
sudo mount -o remount,usrquota,grpquota /
Verify the change:
mount | grep ' / '
Expected Output: usrquota,grpquota should appear in the options.
Step 3: Enable Quotas Permanently

Edit /etc/fstab:
sudo nano /etc/fstab
Find the line for / and add usrquota,grpquota to the options:
UUID=... / ext4 defaults,usrquota,grpquota 0 1
Reboot or remount:
sudo mount -o remount /
Step 4: Initialize Quota System

Run:
sudo quotacheck -cugm /
-c: Create quota files.
-u: User quotas.
-g: Group quotas.
-m: Force check on mounted filesystem.
Enable quotas:
sudo quotaon -v /
Task 2: Set Soft and Hard Limits Using edquota

Step 1: Assign Quotas to a User

Use edquota to edit a user’s quota (replace username):
sudo edquota -u username
A text editor will open. Set limits (e.g., 100MB soft limit, 150MB hard limit):
Disk quotas for user username (uid 1001):
  Filesystem  blocks  soft  hard  inodes  soft  hard
  /dev/sda1    0      100000  150000    0      0     0
blocks: Current usage (KB).
soft/hard: Limits in KB (100000KB = 100MB).
Step 2: Verify Quota

Check the user’s quota:
sudo quota -u username
Expected Output: Displays usage and limits.
Step 3: Set Grace Period (Optional)

Set a 7-day grace period for soft limits:
sudo edquota -t
Modify the Time units may be: days, hours, minutes, or seconds line.
Task 3: Automate Quota Management with a Script

Step 1: Create a Script

Open a new file:
nano quota_manager.sh
Paste the following (customize users/limits as needed):
#!/bin/bash
users=("user1" "user2")  # Add usernames
soft_limit=100000        # 100MB in KB
hard_limit=150000        # 150MB in KB

for user in "${users[@]}"; do
  echo "Setting quota for $user..."
  setquota -u "$user" "$soft_limit" "$hard_limit" 0 0 /
done
echo "Quotas configured for all users."
Step 2: Make the Script Executable

Run:
chmod +x quota_manager.sh
Execute the script:
sudo ./quota_manager.sh
Step 3: Verify Automation

Check quotas for all users:
sudo repquota /
