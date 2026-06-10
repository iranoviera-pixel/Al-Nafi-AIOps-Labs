Lab 7: Managing File Permissions

Objectives

By the end of this lab, students will be able to:

Understand Linux file permissions and ownership.
Modify file permissions using chmod.
Change file ownership with chown.
Assign group ownership using chgrp.
Automate permission changes with a shell script.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line.
Access to a Linux-based system (Al Nafi provides cloud machines—click Start Lab to begin).
A terminal window open and ready for commands.
Task 1: Modify File Permissions with chmod

Objective: Learn to change file permissions using symbolic and numeric modes.

Subtasks

Create a test file
Run:

touch testfile.txt
Expected Outcome: A file named testfile.txt is created.

Check current permissions
Run:

ls -l testfile.txt
Expected Outcome: Displays permissions (e.g., -rw-r--r--).

Add execute permission for the owner (symbolic mode)
Run:

chmod u+x testfile.txt
Expected Outcome: ls -l shows -rwxr--r--.

Remove read access for others (numeric mode)
Run:

chmod 744 testfile.txt
Expected Outcome: Permissions change to -rwxr-----.

Troubleshooting Tip: If you see "Permission denied," ensure you own the file (use ls -l to check).

Task 2: Change Ownership with chown

Objective: Transfer file ownership to another user.

Subtasks

Create a dummy user (if needed)
Run:

sudo adduser demo_user
Note: Skip if using Al Nafi’s pre-configured machine.

Change file ownership
Run:

sudo chown demo_user testfile.txt
Expected Outcome: ls -l shows demo_user as the owner.

Key Concept: Use sudo for chown as it requires root privileges.

Task 3: Assign Group Ownership with chgrp

Objective: Modify the group associated with a file.

Subtasks

Create a dummy group (if needed)
Run:
sudo addgroup demo_group
Assign the group to the file
Run:
sudo chgrp demo_group testfile.txt
Expected Outcome: ls -l shows demo_group as the group.
Task 4: Automate Permissions with a Script

Objective: Write a script to apply permissions recursively to a directory.

Subtasks

Create a directory and sample files
Run:

mkdir testdir && touch testdir/file{1..3}.txt
Write the script (permission_script.sh)

#!/bin/bash
chmod -R 750 testdir  # Gives owner rwx, group r-x, others no access
echo "Permissions updated for all files in testdir."
Make the script executable
Run:

chmod +x permission_script.sh
Run the script

./permission_script.sh
Expected Outcome: All files in testdir now have 750 permissions.
