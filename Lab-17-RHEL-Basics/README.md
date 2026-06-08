Lab 17: Configuring Role-Based Access Control (RBAC) with SELinux

Objectives

By the end of this lab, students will be able to:

Understand SELinux and its role in enforcing RBAC.
Configure SELinux policies to implement role-based access control.
Create and assign custom SELinux roles for users.
Verify and troubleshoot SELinux RBAC configurations.
Prerequisites

Before starting this lab, ensure you have:

Basic Linux command-line knowledge (e.g., ls, cd, sudo).
A Linux-based system with SELinux installed and enabled (Al Nafi’s cloud machine meets this requirement).
Administrative (sudo) privileges to modify SELinux policies.
Note: Al Nafi provides pre-configured Linux cloud machines. Click Start Lab to begin—no VM setup required!

Task 1: Research SELinux and RBAC Features

Subtasks

Understand SELinux Modes
SELinux operates in three modes:

Enforcing: Policies are actively enforced.
Permissive: Policies are logged but not enforced.
Disabled: SELinux is turned off.
Run the following command to check the current mode:

sestatus
Expected Output:

SELinux status:                 enabled
SELinuxfs mount:                /sys/fs/selinux
Current mode:                   enforcing
Learn About RBAC in SELinux
SELinux uses:

Roles: Define what a user/process can do (e.g., sysadm_r for admins).
Types: Labels for files/processes (e.g., httpd_t for web server).
Users: Mapped to roles (e.g., user_u).
List SELinux users and roles:

semanage user -l
Task 2: Configure SELinux for RBAC

Subtasks

Switch to Permissive Mode (Temporarily)
Avoid lockouts while configuring:

sudo setenforce 0
Create a Custom SELinux User
Example: Create webadmin_u for web administrators:

sudo semanage user -a -R "staff_r system_r" -L s0 -r s0 webadmin_u
-R: Assign roles (staff_r and system_r).
-L/-r: Set sensitivity/range (default s0).
Map a Linux User to the SELinux User
Assign webadmin_u to the Linux user alice:

sudo semanage login -a -s webadmin_u alice
Verify the Mapping

sudo semanage login -l
Expected Output:

Login Name      SELinux User   MLS/MCS Range
alice           webadmin_u     s0
Task 3: Create Custom SELinux Roles

Subtasks

Write a Script to Automate Role Creation
Create custom_roles.sh:

#!/bin/bash
# Define a new role 'dev_r' with web server access
sudo semanage user -a -R "user_r webadm_r" -L s0 -r s0 dev_u
sudo semanage login -a -s dev_u bob
echo "Custom role 'dev_r' created and assigned to user 'bob'."
Make the Script Executable

chmod +x custom_roles.sh
sudo ./custom_roles.sh
Test the New Role
Switch to bob and verify permissions:

sudo su - bob
id -Z
Expected Output:

dev_u:staff_r:staff_t:s0
Troubleshooting Tips

Permission Denied?
Check SELinux denials:
 sudo ausearch -m avc -ts recent
Role Not Applied?
Ensure the user is logged out and back in after assignment.
