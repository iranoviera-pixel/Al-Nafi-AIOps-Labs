Lab 55: Using cgroups for Resource Management

Objectives

By the end of this lab, you will:

Understand the purpose and benefits of cgroups (control groups) in Linux.
Learn how to create and configure cgroups to limit CPU and memory usage.
Write a script to automate cgroup management for specific applications.
Prerequisites

Before starting, ensure you have:

A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with the Linux command line.
Administrative/sudo privileges (required for cgroup operations).
Task 1: Configure cgroups to Limit Resources for Processes

Step 1: Verify cgroups Support

Open a terminal.
Run:
mount | grep cgroup
Expected Output: Lists mounted cgroup subsystems (e.g., cpu, memory).
Step 2: Install cgroups Tools (if needed)

On Debian/Ubuntu:

sudo apt install cgroup-tools
On CentOS/RHEL:

sudo yum install libcgroup-tools
Troubleshooting Tip:

If mount shows no cgroups, enable them in the kernel:

sudo modprobe cgroup
Task 2: Create a cgroup for CPU and Memory Management

Step 1: Create a cgroup

Create a cgroup named lab_group:
sudo cgcreate -g cpu,memory:/lab_group
Step 2: Set CPU and Memory Limits

Limit CPU usage to 50% for processes in lab_group:

echo 50000 | sudo tee /sys/fs/cgroup/cpu/lab_group/cpu.cfs_quota_us
(Note: cpu.cfs_quota_us=50000 sets a 50% limit relative to cpu.cfs_period_us [default: 100000]).

Limit memory to 512MB:

echo 512M | sudo tee /sys/fs/cgroup/memory/lab_group/memory.limit_in_bytes
Step 3: Test the cgroup

Run a stress test in the cgroup:
sudo cgexec -g cpu,memory:lab_group stress --cpu 1 --vm 1 --vm-bytes 256M
Monitor resource usage in another terminal:
top
Expected Outcome: The stress process should not exceed 50% CPU or 512MB memory.
Task 3: Automate cgroup Management with a Script

Step 1: Write a Bash Script

Create manage_cgroup.sh:

#!/bin/bash
CGROUP_NAME="app_group"
RESOURCE_LIMIT_CPU="30000"  # 30% CPU
RESOURCE_LIMIT_MEM="256M"   # 256MB memory

# Create cgroup
sudo cgcreate -g cpu,memory:/$CGROUP_NAME

# Set limits
echo $RESOURCE_LIMIT_CPU | sudo tee /sys/fs/cgroup/cpu/$CGROUP_NAME/cpu.cfs_quota_us > /dev/null
echo $RESOURCE_LIMIT_MEM | sudo tee /sys/fs/cgroup/memory/$CGROUP_NAME/memory.limit_in_bytes > /dev/null

echo "Cgroup '$CGROUP_NAME' created with CPU limit: $RESOURCE_LIMIT_CPU and memory limit: $RESOURCE_LIMIT_MEM."
Step 2: Run the Script

Make it executable:
chmod +x manage_cgroup.sh
Execute:
sudo ./manage_cgroup.sh
Step 3: Verify Automation

Check the cgroup:

ls /sys/fs/cgroup/cpu/app_group/
Expected Outcome: Files like cpu.cfs_quota_us reflect the limits set.
