Lab 27: Setting Up and Managing ACLs

Objectives

By the end of this lab, you will be able to:

Understand Access Control Lists (ACLs) and their purpose in Linux.
Use setfacl to configure ACLs for files and directories.
View ACLs using getfacl.
Automate ACL configuration using a Bash script.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line.
A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Permissions to execute administrative commands (use sudo where required).
Task 1: Set Up ACLs Using setfacl

Step 1: Verify ACL Support

Open the terminal.
Check if your filesystem supports ACLs:
mount | grep acl
Expected Output: Look for acl in the options (e.g., rw,relatime,acl).
Troubleshooting: If not enabled, remount the filesystem:
sudo mount -o remount,acl /
Step 2: Create a Test File and Directory

Create a directory and file:
mkdir ~/test_dir
touch ~/test_dir/test_file.txt
Step 3: Grant ACL Permissions

Give a user-specific permission (replace username with a real user):

setfacl -m u:username:rwx ~/test_dir/test_file.txt
-m: Modify ACL.
u:username:rwx: Grants read/write/execute to username.
Verify:

getfacl ~/test_dir/test_file.txt
Expected Output:
user:username:rwx
Task 2: View ACLs Using getfacl

Step 1: Check Default ACLs

View ACLs for the test file:
getfacl ~/test_dir/test_file.txt
Expected Output: Displays owner, group, and any custom ACLs.
Step 2: Check Directory ACLs

View ACLs for the directory:
getfacl ~/test_dir
Key Concept: Directories can have default ACLs inherited by new files.
Task 3: Automate ACL Configuration with a Script

Step 1: Create a Script

Open a new file acl_manager.sh:

nano ~/acl_manager.sh
Paste the script:

#!/bin/bash
# Assigns read/write to a group for multiple directories
GROUP="developers"
DIRS=("/path/to/dir1" "/path/to/dir2")"

for dir in "${DIRS[@]}"; do
  setfacl -Rm g:$GROUP:rwx "$dir"
  echo "ACL set for $dir"
done
Explanation:
-R: Recursive (applies to subdirectories).
g:$GROUP:rwx: Grants rwx to the developers group.
Make the script executable:

chmod +x ~/acl_manager.sh
Step 2: Run the Script

Execute with sudo:
sudo ./acl_manager.sh
Expected Outcome: Script applies ACLs to all directories listed.
