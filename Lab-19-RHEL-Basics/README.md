Lab 19: Troubleshooting SUDO and SELinux Issues

Objectives

By the end of this lab, you will be able to:

Analyze SUDO and SELinux logs to diagnose access issues.
Create a script to identify common SUDO configuration problems.
Resolve SELinux denials using audit2allow.
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge (e.g., ls, cat, sudo).
A Linux-based system (Al Nafi’s cloud machine is ready-to-use—click Start Lab).
Installed packages: sudo, auditd, setroubleshoot (pre-installed on most distributions).
Task 1: Troubleshoot SUDO and SELinux Logs

Step 1: Check SUDO Logs

SUDO logs all attempts (successful/failed) in /var/log/secure (RHEL/CentOS) or /var/log/auth.log (Debian/Ubuntu).

Command:

sudo cat /var/log/secure | grep sudo
OR

sudo cat /var/log/auth.log | grep sudo
Expected Output:
Log entries showing user attempts, e.g.,

Jan 1 10:00:00 hostname sudo: alice : user NOT in sudoers ; TTY=pts/0 ; PWD=/home/alice
Troubleshooting Tip: If no logs appear, ensure sudo logging is enabled in /etc/sudoers (default: enabled).

Step 2: Analyze SELinux Denials

SELinux logs denials in /var/log/audit/audit.log.

Command:

sudo cat /var/log/audit/audit.log | grep AVC
Expected Output:

type=AVC msg=audit(123456.789:123): avc: denied { read } for pid=1234 comm="nginx" name="index.html" dev="sda1" ino=1234 scontext=system_u:system_r:httpd_t:s0 tcontext=unconfined_u:object_r:default_t:s0 tclass=file
Key Concept:

scontext: Subject (process) context.
tcontext: Target (file/port) context.
Task 2: Script for SUDO Configuration Checks

Step 1: Create the Script

Write a script (check_sudo.sh) to verify:

User’s SUDO privileges.
Syntax errors in /etc/sudoers.
Script:

#!/bin/bash

# Check if user is in sudoers  
echo "Checking sudo privileges for $USER..."  
sudo -l || echo "Error: User $USER not in sudoers or misconfigured."  

# Validate sudoers file syntax  
echo "Checking /etc/sudoers syntax..."  
sudo visudo -cf /etc/sudoers  
Run the Script:

chmod +x check_sudo.sh  
./check_sudo.sh  
Expected Output:

User alice may run the following commands on hostname: (ALL) ALL  
/etc/sudoers: parsed OK  
Task 3: Resolve SELinux Denials with audit2allow

Step 1: Generate a Custom SELinux Policy

Find the denial in /var/log/audit/audit.log.
Create a policy module:
Commands:

# Capture denial (replace with your AVC error)  
sudo grep AVC /var/log/audit/audit.log | audit2allow -m mypolicy > mypolicy.te  

# Compile and load the module  
sudo checkmodule -M -m -o mypolicy.mod mypolicy.te  
sudo semodule_package -o mypolicy.pp -m mypolicy.mod  
sudo semodule -i mypolicy.pp  
Expected Outcome:
SELinux allows the previously denied action (e.g., Nginx accessing a file`).

Troubleshooting Tip:

Use audit2allow -w to get human-readable explanations of denials.
