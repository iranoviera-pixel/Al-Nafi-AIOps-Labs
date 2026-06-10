Lab 12: Configuring Password Policies and Aging

Objectives

By the end of this lab, students will be able to:

Configure password aging and expiration using the chage command.
Set up password complexity policies in /etc/login.defs.
Write and execute a script to automate password aging for multiple users.
Prerequisites

Before starting this lab, ensure you have:

Basic familiarity with Linux command-line operations.
Access to a Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Administrative/sudo privileges to modify system files.
Task 1: Configure Password Aging with chage

Objective: Set password expiration and aging policies for a user.

Steps:

Open a terminal in your Linux machine.

Check current password aging settings for a user (e.g., user1):

sudo chage -l user1
Expected Output: Displays current password expiration details (e.g., last change, expiry date).
Set password expiration (e.g., force password change every 90 days):

sudo chage -M 90 user1
Explanation: -M sets the maximum number of password validity.
Set account expiration (e.g., warn user 7 days before expiry):

sudo chage -W 7 user1
Explanation: -W sets the warning period.
Verify changes:

sudo chage -l user1
Expected Outcome: Updated values for Maximum number of days and Warning days.
Troubleshooting:

If you see "user 'user1' does not exist," create the user first with sudo adduser user1.
Task 2: Configure Password Complexity in /etc/login.defs

Objective: Enforce password complexity rules system-wide.

Steps:

Open the configuration file:

sudo nano /etc/login.defs
Modify the following parameters (add or uncomment lines):

PASS_MAX_DAYS   90
PASS_MIN_DAYS   1
PASS_WARN_AGE   7
Explanation:
PASS_MAX_DAYS: Maximum password validity (matches Task 1).
PASS_MIN_DAYS: Minimum days between password changes.
PASS_WARN_AGE: Warning period before expiry.
Save the file (Ctrl+O, then Ctrl+X in nano).

Apply changes to existing users (e.g., user1):

sudo chage -M 90 -m 1 -W 7 user1
Verification:

Run sudo chage -l user1 to confirm the new policies.
Task 3: Automate Password Aging with a Script

Objective: Write a script to apply password policies to all users.

Steps:

Create a script file:

sudo nano /usr/local/bin/set_password_policies.sh
Add the following code:

#!/bin/bash
# Set password aging for all users (except system accounts)
for user in $(awk -F: '$3 >= 1000 {print $1}' /etc/passwd); do
  sudo chage -M 90 -m 1 -W 7 "$user"
  echo "Password policies applied to $user"
done
Explanation:
The script loops through users with UID ≥ 1000 (excluding system accounts).
Applies the same policies as Task 1/2.
Make the script executable:

sudo chmod +x /usr/local/bin/set_password_policies.sh
Run the script:

sudo /usr/local/bin/set_password_policies.sh
Expected Output: Confirmation messages for each user.
Troubleshooting:

If the script fails, check permissions with ls -l /usr/local/bin/set_password_policies.sh.
