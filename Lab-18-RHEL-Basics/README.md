Lab 18: Automating SELinux Role Assignment

Objectives

By the end of this lab, you will be able to:

Understand SELinux roles and their importance in Linux security.
Use semanage to assign SELinux roles to users manually.
Automate role assignments based on group membership using a Bash script.
Create a script to audit and update SELinux role assignments.
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge (e.g., sudo, vim, chmod).
A Linux system with SELinux enabled (Al Nafi’s cloud machine provides this).
Administrative privileges (use sudo where required).
The policycoreutils-python-utils package installed (includes semanage).
Note: Al Nafi’s cloud machines come preconfigured with these tools. Click Start Lab to begin.

Task 1: Assign SELinux Roles Using semanage

Step 1: Verify SELinux Status

Open a terminal.
Run:
sestatus
Expected Output:
SELinux status: enabled
If disabled, enable it with sudo setenforce 1.
Step 2: List Existing SELinux Users

Run:
sudo semanage user -l
Expected Output: A table showing SELinux users and their roles (e.g., staff_u).
Step 3: Assign a Role to a Linux User

Assign the staff_u role to user alice:

sudo semanage login -a -s staff_u alice
Explanation:
-a adds a mapping, -s specifies the SELinux user.
Verify the assignment:

sudo semanage login -l | grep alice
Expected Output:
alice staff_u s0-s0:c0.c1023
Task 2: Automate Role Assignment by Group

Step 1: Create a Script

Open a file named assign_roles.sh:
nano assign_roles.sh
Paste this script:
#!/bin/bash
# Assign SELinux roles based on group membership

GROUP="developers"  # Group to check
ROLE="staff_u"      # SELinux role to assign

for USER in $(getent group $GROUP | cut -d: -f4 | tr ',' ' '); do
  echo "Assigning $ROLE to $USER"
  sudo semanage login -a -s $ROLE $USER || echo "Failed to assign role to $USER"
done
Explanation:
The script checks all members of the developers group and assigns them the staff_u role.
Step 2: Make the Script Executable

Run:
chmod +x assign_roles.sh
Step 3: Test the Script

Create a test group and user:
sudo groupadd developers
sudo useradd -G developers bob
Execute the script:
./assign_roles.sh
Expected Output:
Assigning staff_u to bob
Task 3: Audit and Update Role Assignments

Step 1: Create an Audit Script

Open audit_roles.sh:
nano audit_roles.sh
Paste this script:
#!/bin/bash
# Audit and correct SELinux role assignments

ROLE="staff_u"  # Expected role

for USER in $(getent passwd | cut -d: -f1); do
  CURRENT_ROLE=$(sudo semanage login -l | grep "^$USER " | awk '{print $2}')
  if [ "$CURRENT_ROLE" != "$ROLE" ]; then
    echo "Updating $USER from $CURRENT_ROLE to $ROLE"
    sudo semanage login -m -s $ROLE $USER
  fi
done
Explanation:
The script ensures all users have the staff_u role, updating mismatches.
Step 2: Run the Audit

Make the script executable and run it:
chmod +x audit_roles.sh
./audit_roles.sh
Expected Output:
Lists users with updated roles (if any).
Troubleshooting Tips

Permission Denied: Use sudo for semanage commands.
User Not Found: Ensure users exist (getent passwd).
SELinux Disabled: Enable it with sudo setenforce 1.
