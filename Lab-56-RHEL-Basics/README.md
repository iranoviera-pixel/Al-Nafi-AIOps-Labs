Lab 56: Setting Resource Limits with ulimits

Objectives

By the end of this lab, you will be able to:

Understand the concept of resource limits in Linux.
Use the ulimit command to view and set user/process resource limits.
Differentiate between hard and soft limits.
Configure file descriptor and memory limits for processes.
Write a script to enforce ulimit restrictions for specific users or groups.
Prerequisites

Before starting this lab, you should have:

Basic familiarity with Linux command line.
Access to a Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Permission to execute administrative commands (sudo access may be required for some tasks).
Task 1: Use ulimit to Set and View User Resource Limits

Step 1: View Current Limits

Open a terminal in your Linux environment.
Run the following command to view all current resource limits for your user:
ulimit -a
Expected Output:
A list of resource settings (e.g., file descriptors, stack size, CPU time).
Step 2: View Specific Limits

To check the maximum number of open file descriptors (soft limit), run:
ulimit -n
To check the hard limit for file descriptors, run:
ulimit -Hn
Key Concept:
Soft Limit: The effective limit enforced for the current user/process.
Hard Limit: The maximum value the soft limit can be raised to (requires root/sudo).
Task 2: Set Hard and Soft Limits for Processes

Step 1: Set a Temporary Soft Limit

To temporarily increase the open file limit to 2048 (for the current session), run:
ulimit -n 2048
Verify the change:
ulimit -n
Expected Outcome: The output should show 2048.
Step 2: Set a Hard Limit (Requires Sudo)

Edit the system-wide limits configuration file:

sudo nano /etc/security/limits.conf
Add the following lines to set hard/soft limits for a user (replace username with your actual username):

username  soft  nofile  4096
username  hard  nofile  8192
Explanation:

nofile: Limits the number of open files.
soft: Applies to the user by default.
hard: Maximum allowable value.
Save the file and log out/login for changes to take effect.

Step 3: Verify Permanent Limits

After relogging, verify the new limits:
ulimit -n      # Soft limit (should show 4096)
ulimit -Hn     # Hard limit (should show 8192)
Task 3: Write a Script to Enforce ulimit Restrictions

Step 1: Create a Bash Script

Open a new file named set_ulimits.sh:
nano set_ulimits.sh
Add the following script to enforce limits for a specific user (e.g., "developer"):
#!/bin/bash
USER="developer"
SOFT_LIMIT=4096
HARD_LIMIT=8192

echo "$USER soft nofile $SOFT_LIMIT" | sudo tee -a /etc/security/limits.conf
echo "$USER hard nofile $HARD_LIMIT" | sudo tee -a /etc/security/limits.conf

echo "Ulimits set for $USER: Soft=$SOFT_LIMIT, Hard=$HARD_LIMIT"
Save the file and make it executable:
chmod +x set_ulimits.sh
Step 2: Run the Script

Execute the script with sudo:
sudo ./set_ulimits.sh
Expected Outcome:
Confirmation message showing the new limits for the user.
