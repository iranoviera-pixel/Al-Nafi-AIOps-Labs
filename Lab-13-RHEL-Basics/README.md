Lab 13: Configuring SUDO for User Permissions

Objectives

By the end of this lab, students will be able to:

Understand the purpose and importance of sudo in Linux systems.
Safely modify the /etc/sudoers file using visudo.
Create custom sudo rules for specific users or groups.
Automate sudo access for multiple users using a script.
Prerequisites

Before starting this lab, ensure you have:

A Linux-based system (provided by Al Nafi's cloud machines—click Start Lab to begin).
Basic familiarity with Linux command-line operations.
A user account with sudo privileges (for initial setup).
Task 1: Modify the /etc/sudoers File Using visudo

Why Use visudo?

The /etc/sudoers file controls sudo permissions. Editing it directly with a text editor can cause syntax errors, which may lock you out of sudo access. visudo validates syntax before saving.

Steps:

Open the sudoers file:

sudo visudo
This opens the file in the default editor (usually nano or vi).
Navigate to the "User Privilege Specification" section:

Look for lines like:
root    ALL=(ALL:ALL) ALL
Add a new rule (e.g., for user alice):

alice   ALL=(ALL:ALL) ALL
This grants alice full sudo access.
Save and exit:

In nano: Press Ctrl+O, then Enter, then Ctrl+X.
In vi: Press :wq, then Enter.
Expected Outcome:

User alice can now run commands with sudo.
Troubleshooting:

If you get a syntax error, visudo will warn you. Do not force-save; fix the error first.
Task 2: Create a Sudo Rule for Specific Commands

Scenario:

Allow a group (developers) to only run apt update and systemctl restart commands with sudo.

Steps:

Create the group (if it doesn’t exist):

sudo groupadd developers
Add users to the group (e.g., bob):

sudo usermod -aG developers bob
Edit /etc/sudoers:

sudo visudo
Add this rule:

%developers ALL=(root) /usr/bin/apt update, /usr/bin/systemctl restart *
% indicates a group.
Commands must use full paths (find them with which <command>).
Save and exit.

Verify:

Switch to bob and test:
sudo apt update  # Should work
sudo ls /root    # Should fail (not allowed)
Task 3: Script to Grant Sudo Access to Multiple Users

Script Purpose:

Automate adding users to a sudoers rule file in /etc/sudoers.d/ (best practice for custom rules).

Steps:

Create a script file:

nano add_sudo_users.sh
Paste this code:

#!/bin/bash
# Define users and commands
USERS=("user1" "user2" "user3")
COMMANDS="/usr/bin/apt update, /usr/bin/systemctl restart *"

# Create a custom sudoers file
for user in "${USERS[@]}"; do
  echo "$user ALL=(root) $COMMANDS" | sudo tee /etc/sudoers.d/$user
done

# Set correct permissions
sudo chmod 440 /etc/sudoers.d/*
Make the script executable:

chmod +x add_sudo_users.sh
Run the script:

sudo ./add_sudo_users.sh
Expected Outcome:

Users user1, user2, and user3 can now run the specified commands with sudo.
Troubleshooting:

If users report "permission denied," check /etc/sudoers.d/ file permissions (must be 440).
