Lab 43: Understanding SELinux Modes and Contexts

Objectives

By the end of this lab, students will:

Understand the three SELinux modes: Enforcing, Permissive, and Disabled.
Check SELinux status and mode using sestatus.
Write and execute a Bash script to switch between SELinux modes and display context information.
Prerequisites

Before starting, ensure you have:

A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with the Linux command line.
Administrative (root) access to modify SELinux settings (use sudo).
Task 1: Learn SELinux Modes

Key Concepts

Enforcing: SELinux actively enforces policies, blocking unauthorized actions.
Permissive: SELinux logs policy violations but does not block them (useful for troubleshooting).
Disabled: SELinux is turned off entirely (requires reboot).
Subtask 1.1: Check Current SELinux Mode

Open a terminal.
Run:
sestatus
Expected Output:
SELinux status:                 enabled  
SELinuxfs mount:                /sys/fs/selinux  
Current mode:                   enforcing  
...  
Subtask 1.2: Temporarily Change SELinux Mode

Switch to Permissive mode:

sudo setenforce 0
Verify:

getenforce
Expected Output: Permissive

Switch back to Enforcing:

sudo setenforce 1
Troubleshooting:

If setenforce fails, ensure SELinux is not disabled in /etc/selinux/config.
Task 2: Check SELinux Contexts

Subtask 2.1: View File Context

Create a test file:
touch ~/testfile.txt
Check its SELinux context:
ls -Z ~/testfile.txt
Expected Output:
-rw-r--r--. user user unconfined_u:object_r:user_home_t:s0 testfile.txt  
Subtask 2.2: View Process Context

Check the Apache (httpd) process context (if installed):
ps -eZ | grep httpd
Expected Output: Contexts like system_u:system_r:httpd_t:s0.
Task 3: Script to Switch Modes and Display Contexts

Subtask 3.1: Write the Script

Create a script selinux_manager.sh:

#!/bin/bash  
echo "Current SELinux Mode: $(getenforce)"  
echo "Switching to Permissive Mode..."  
sudo setenforce 0  
echo "New Mode: $(getenforce)"  
echo "Sample File Context:"  
touch /tmp/test_selinux && ls -Z /tmp/test_selinux  
Make it executable:

chmod +x selinux_manager.sh
Subtask 3.2: Run the Script

Execute:
./selinux_manager.sh
Expected Output:
Current SELinux Mode: Enforcing  
Switching to Permissive Mode...  
New Mode: Permissive  
Sample File Context:  
-rw-r--r--. user user unconfined_u:object_r:user_tmp_t:s0 /tmp/test_selinux  
