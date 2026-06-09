Lab 14: Automating User and Group Management with Scripts

Objectives

By the end of this lab, students will be able to:

Write Bash scripts to automate user and group creation in Linux.
Assign users to multiple groups using scripts.
Modify user permissions programmatically for bulk of users.
Understand the importance of automation in system administration.
Prerequisites

Before starting this lab, ensure you have:

Basic familiarity with Linux command line (e.g., cd, mkdir, sudo).
Knowledge of basic Bash scripting (e.g., variables, loops).
Access to a Linux-based cloud machine (provided by Al Nafi—click Start Lab to launch).
Sudo privileges (configured automatically in the provided cloud machine).
Lab Setup

Start your cloud machine:
Click Start Lab in your Al Nafi dashboard to launch a pre-configured Linux (Ubuntu) machine.
Open Terminal:
Use the terminal emulator in the cloud environment (e.g., GNOME Terminal).
Task 1: Create Users and Groups with a Script

Subtasks

Create a script file:
nano user_group_creator.sh
Write the script:
#!/bin/bash

# Define users and groups
USERS=("alice" "bob" "charlie")
GROUPS=("developers" "admins" "testers")

# Create groups
for group in "${GROUPS[@]}"; do
    sudo groupadd "$group"
    echo "Created group: $group"
done

# Create users and assign default group
for user in "${USERS[@]}"; do
    sudo useradd -m -s /bin/bash -G developers "$user"
    echo "Created user: $user"
done

echo "User and group creation complete!"
Make the script executable:
chmod +x user_group_creator.sh
Run the script:
sudo ./user_group_creator.sh
Expected Output

Groups developers, admins, and testers are created.
Users alice, bob, and charlie are created with /bin/bash shell and added to the developers group.
Troubleshooting

If you get a "Permission denied" error, ensure the script is executable (chmod +x).
If a user/group already exists, use sudo userdel or sudo groupdel to remove them first.
Task 2: Assign Users to Multiple Groups

Subtasks

Create a script file:
nano group_assigner.sh
Write the script:
#!/bin/bash

# Assign users to additional groups
sudo usermod -aG admins alice
sudo usermod -aG testers bob
sudo usermod -aG admins,testers charlie

echo "Users assigned to groups successfully!"
Run the script:
sudo ./group_assigner.sh
Verification

Check group assignments with:

groups alice  # Should show: alice developers admins
Key Concept

usermod -aG appends groups to a user without removing existing ones.
Task 3: Modify User Permissions Automatically

Subtasks

Create a directory for testing:
sudo mkdir /shared_data
sudo chown root:developers /shared_data
sudo chmod 770 /shared_data
Verify permissions:
ls -ld /shared_data  # Should show drwxrwx--- 
Explanation

chown sets ownership to root:developers.
chmod 770 gives read/write/execute to owner/group, nothing to others.
