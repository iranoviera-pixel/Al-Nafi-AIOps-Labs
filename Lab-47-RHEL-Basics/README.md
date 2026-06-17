Lab 47: Implementing SELinux Custom Policies

Objectives

By the end of this lab, students will be able to:

Understand the fundamentals of SELinux policy creation and customization
Create custom SELinux policy modules using audit2allow and semanage tools
Apply and test custom SELinux policies to enforce specific access controls
Troubleshoot SELinux policy issues and verify policy effectiveness
Implement security best practices using custom SELinux policies
Prerequisites

Before starting this lab, students should have:

Basic understanding of Linux command line operations
Familiarity with file permissions and ownership concepts
Basic knowledge of SELinux concepts (contexts, domains, types)
Understanding of system administration fundamentals
Access to a Linux system with SELinux enabled (CentOS/RHEL/Fedora recommended)
Ready-to-Use Cloud Machines

Al Nafi provides pre-configured Linux-based cloud machines with SELinux enabled and all necessary tools pre-installed. Simply click Start Lab to access your environment - no need to build your own virtual machine or install additional software.

Your cloud machine includes:

CentOS/RHEL system with SELinux in enforcing mode
All required SELinux policy development tools
Sample applications for testing
Administrative privileges for policy management
Task 1: Research SELinux Policy Creation and Customization

Subtask 1.1: Understanding SELinux Policy Architecture

First, let's explore the current SELinux configuration and understand how policies work.

Step 1: Check SELinux status and mode

# Check current SELinux status
sestatus

# View current enforcement mode
getenforce

# List available SELinux booleans
getsebool -a | head -10
Step 2: Examine existing SELinux policies

# List installed policy modules
semodule -l | head -10

# View SELinux contexts for common directories
ls -Z /var/www/
ls -Z /home/
ls -Z /tmp/
Step 3: Understand SELinux policy components

# View available SELinux types
seinfo -t | head -20

# View available SELinux domains
seinfo -d | head -20

# Check current user context
id -Z
Subtask 1.2: Exploring Policy Development Tools

Step 1: Install policy development tools (if not already installed)

# Install SELinux policy development packages
sudo yum install -y policycoreutils-python-utils selinux-policy-devel

# Verify installation
which audit2allow
which semanage
which checkmodule
Step 2: Understand audit log analysis

# View recent SELinux denials
sudo ausearch -m AVC -ts recent

# Check SELinux alert logs
sudo tail -f /var/log/audit/audit.log | grep AVC
Task 2: Write and Apply a Custom SELinux Policy Module

Subtask 2.1: Create a Test Application Scenario

We'll create a custom web application that needs special SELinux permissions.

Step 1: Create a test web application directory

# Create application directory
sudo mkdir -p /opt/mywebapp
sudo mkdir -p /opt/mywebapp/data
sudo mkdir -p /opt/mywebapp/logs

# Create a simple test script
sudo tee /opt/mywebapp/webapp.py << 'EOF'
#!/usr/bin/env python3
import os
import time

# Test application that writes to data and log directories
def main():
    # Write to data directory
    with open('/opt/mywebapp/data/app_data.txt', 'w') as f:
        f.write(f"Application data written at {time.ctime()}\n")
    
    # Write to log directory
    with open('/opt/mywebapp/logs/app.log', 'a') as f:
        f.write(f"Log entry at {time.ctime()}\n")
    
    print("Application executed successfully")

if __name__ == "__main__":
    main()
EOF

# Make script executable
sudo chmod +x /opt/mywebapp/webapp.py
Step 2: Set initial ownership and permissions

# Set ownership
sudo chown -R apache:apache /opt/mywebapp

# Set basic permissions
sudo chmod 755 /opt/mywebapp
sudo chmod 755 /opt/mywebapp/data
sudo chmod 755 /opt/mywebapp/logs
Subtask 2.2: Generate SELinux Denials for Policy Creation

Step 1: Run the application to generate denials

# Try to run the application as apache user
sudo -u apache python3 /opt/mywebapp/webapp.py

# Check for SELinux denials
sudo ausearch -m AVC -ts recent
Step 2: Create a systemd service for our application

# Create systemd service file
sudo tee /etc/systemd/system/mywebapp.service << 'EOF'
[Unit]
Description=My Web Application
After=network.target

[Service]
Type=simple
User=apache
Group=apache
ExecStart=/usr/bin/python3 /opt/mywebapp/webapp.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and try to start service
sudo systemctl daemon-reload
sudo systemctl start mywebapp
sudo systemctl status mywebapp
Subtask 2.3: Create Custom SELinux Policy Module

Step 1: Collect SELinux denials

# Generate more comprehensive denials
sudo systemctl stop mywebapp
sudo systemctl start mywebapp
sleep 5
sudo systemctl stop mywebapp

# Extract AVC denials for our application
sudo ausearch -m AVC -ts recent | grep mywebapp > /tmp/mywebapp_denials.txt

# If no specific denials, create generic ones
sudo ausearch -m AVC -ts today | tail -20 > /tmp/mywebapp_denials.txt
Step 2: Generate policy module using audit2allow

# Create policy module from denials
sudo audit2allow -i /tmp/mywebapp_denials.txt -m mywebapp_policy > mywebapp_policy.te

# If no denials found, create a basic policy template
if [ ! -s mywebapp_policy.te ]; then
    cat > mywebapp_policy.te << 'EOF'
module mywebapp_policy 1.0;

require {
    type httpd_t;
    type admin_home_t;
    type user_home_dir_t;
    type usr_t;
    class file { create write open read getattr };
    class dir { search write add_name };
}

# Allow httpd to write to our application directories
allow httpd_t usr_t:file { create write open read getattr };
allow httpd_t usr_t:dir { search write add_name };
EOF
fi

# View the generated policy
cat mywebapp_policy.te
Step 3: Create a more comprehensive custom policy

# Create enhanced policy module
cat > mywebapp_custom.te << 'EOF'
module mywebapp_custom 1.0;

require {
    type httpd_t;
    type httpd_exec_t;
    type usr_t;
    type bin_t;
    type shell_exec_t;
    type python3_exec_t;
    class file { execute execute_no_trans create write open read getattr ioctl lock };
    class dir { search write add_name remove_name };
    class process { transition };
}

# Define new type for our application
type mywebapp_t;
type mywebapp_exec_t;
type mywebapp_data_t;
type mywebapp_log_t;

# File context rules
files_type(mywebapp_data_t)
files_type(mywebapp_log_t)
files_type(mywebapp_exec_t)

# Domain transition rules
domain_type(mywebapp_t)
domain_entry_file(mywebapp_t, mywebapp_exec_t)

# Allow domain transition
allow httpd_t mywebapp_exec_t:file { execute read open getattr };
allow httpd_t mywebapp_t:process transition;
allow mywebapp_t mywebapp_exec_t:file entrypoint;

# Allow application to access its data and log directories
allow mywebapp_t mywebapp_data_t:file { create write open read getattr ioctl lock };
allow mywebapp_t mywebapp_data_t:dir { search write add_name remove_name };
allow mywebapp_t mywebapp_log_t:file { create write open read getattr ioctl lock };
allow mywebapp_t mywebapp_log_t:dir { search write add_name remove_name };

# Allow python execution
allow mywebapp_t python3_exec_t:file { execute execute_no_trans };
allow mywebapp_t bin_t:file { execute execute_no_trans };
EOF
Subtask 2.4: Compile and Install the Policy Module

Step 1: Compile the policy module

# Compile the policy module
checkmodule -M -m -o mywebapp_custom.mod mywebapp_custom.te

# Create policy package
semodule_package -o mywebapp_custom.pp -m mywebapp_custom.mod
Step 2: Install the policy module

# Install the custom policy module
sudo semodule -i mywebapp_custom.pp

# Verify installation
semodule -l | grep mywebapp
Step 3: Create file context definitions

# Create file context file
cat > mywebapp_custom.fc << 'EOF'
/opt/mywebapp(/.*)?                    gen_context(system_u:object_r:mywebapp_exec_t,s0)
/opt/mywebapp/webapp\.py               gen_context(system_u:object_r:mywebapp_exec_t,s0)
/opt/mywebapp/data(/.*)?               gen_context(system_u:object_r:mywebapp_data_t,s0)
/opt/mywebapp/logs(/.*)?               gen_context(system_u:object_r:mywebapp_log_t,s0)
EOF

# Add file contexts to SELinux
sudo semanage fcontext -a -t mywebapp_exec_t "/opt/mywebapp(/.*)?"
sudo semanage fcontext -a -t mywebapp_exec_t "/opt/mywebapp/webapp\.py"
sudo semanage fcontext -a -t mywebapp_data_t "/opt/mywebapp/data(/.*)?"
sudo semanage fcontext -a -t mywebapp_log_t "/opt/mywebapp/logs(/.*)?"
Step 4: Apply file contexts

# Restore file contexts
sudo restorecon -Rv /opt/mywebapp/

# Verify contexts
ls -Z /opt/mywebapp/
ls -Z /opt/mywebapp/data/
ls -Z /opt/mywebapp/logs/
Task 3: Test the Policy Module

Subtask 3.1: Verify Policy Installation and Context Application

Step 1: Check policy module status

# List custom policy modules
semodule -l | grep mywebapp

# Check policy module details
semodule -l -v | grep mywebapp

# Verify file contexts are applied
semanage fcontext -l | grep mywebapp
Step 2: Test file context restoration

# Check current contexts
ls -Z /opt/mywebapp/webapp.py
ls -Z /opt/mywebapp/data/
ls -Z /opt/mywebapp/logs/

# If contexts are not correct, restore them
sudo restorecon -Rv /opt/mywebapp/

# Verify contexts again
ls -Z /opt/mywebapp/webapp.py
Subtask 3.2: Test Application Functionality

Step 1: Test direct application execution

# Test running the application directly
sudo -u apache python3 /opt/mywebapp/webapp.py

# Check if files were created successfully
ls -la /opt/mywebapp/data/
ls -la /opt/mywebapp/logs/

# Check for any new SELinux denials
sudo ausearch -m AVC -ts recent
Step 2: Test systemd service

# Start the service
sudo systemctl start mywebapp

# Check service status
sudo systemctl status mywebapp

# Check logs
sudo journalctl -u mywebapp -n 10

# Stop the service
sudo systemctl stop mywebapp
Subtask 3.3: Validate Access Controls

Step 1: Test unauthorized access prevention

# Create a test script that tries unauthorized access
cat > /tmp/test_unauthorized.py << 'EOF'
#!/usr/bin/env python3
import os

try:
    # Try to access system directories (should be denied)
    with open('/etc/shadow', 'r') as f:
        print("ERROR: Unauthorized access succeeded!")
except PermissionError:
    print("GOOD: Unauthorized access properly denied")
except Exception as e:
    print(f"Access denied: {e}")

try:
    # Try to write to unauthorized location
    with open('/etc/test_file', 'w') as f:
        f.write("test")
    print("ERROR: Unauthorized write succeeded!")
except PermissionError:
    print("GOOD: Unauthorized write properly denied")
except Exception as e:
    print(f"Write denied: {e}")
EOF

chmod +x /tmp/test_unauthorized.py

# Run unauthorized access test
sudo -u apache python3 /tmp/test_unauthorized.py
Step 2: Monitor and analyze SELinux activity

# Monitor SELinux denials in real-time (run in separate terminal)
sudo tail -f /var/log/audit/audit.log | grep AVC &

# Run various tests
sudo -u apache python3 /opt/mywebapp/webapp.py
sudo systemctl start mywebapp
sleep 5
sudo systemctl stop mywebapp

# Stop monitoring
sudo pkill -f "tail -f /var/log/audit/audit.log"
Subtask 3.4: Policy Refinement and Troubleshooting

Step 1: Identify and resolve policy issues

# Check for recent denials
sudo ausearch -m AVC -ts recent | tail -10

# If denials exist, create additional policy rules
if sudo ausearch -m AVC -ts recent | grep -q denied; then
    echo "Found SELinux denials, generating additional policy..."
    sudo ausearch -m AVC -ts recent | audit2allow -m mywebapp_additional > mywebapp_additional.te
    cat mywebapp_additional.te
fi
Step 2: Create policy debugging tools

# Create a policy testing script
cat > test_policy.sh << 'EOF'
#!/bin/bash

echo "=== SELinux Policy Test Script ==="
echo "1. Checking SELinux status..."
sestatus

echo -e "\n2. Checking custom policy module..."
semodule -l | grep mywebapp

echo -e "\n3. Checking file contexts..."
ls -Z /opt/mywebapp/webapp.py
ls -Z /opt/mywebapp/data/
ls -Z /opt/mywebapp/logs/

echo -e "\n4. Testing application execution..."
sudo -u apache python3 /opt/mywebapp/webapp.py

echo -e "\n5. Checking for recent denials..."
sudo ausearch -m AVC -ts recent | tail -5

echo -e "\n6. Verifying created files..."
if [ -f /opt/mywebapp/data/app_data.txt ]; then
    echo "✓ Data file created successfully"
    ls -Z /opt/mywebapp/data/app_data.txt
else
    echo "✗ Data file creation failed"
fi

if [ -f /opt/mywebapp/logs/app.log ]; then
    echo "✓ Log file created successfully"
    ls -Z /opt/mywebapp/logs/app.log
else
    echo "✗ Log file creation failed"
fi

echo -e "\nPolicy test completed!"
EOF

chmod +x test_policy.sh
./test_policy.sh
Subtask 3.5: Advanced Policy Management

Step 1: Create policy management utilities

# Create policy backup script
cat > backup_policy.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/root/selinux_backups"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

echo "Backing up custom SELinux policies..."
semodule -l | grep mywebapp > $BACKUP_DIR/mywebapp_modules_$DATE.txt
semanage fcontext -l | grep mywebapp > $BACKUP_DIR/mywebapp_contexts_$DATE.txt

# Export policy module
semodule -e mywebapp_custom
cp mywebapp_custom.pp $BACKUP_DIR/mywebapp_custom_$DATE.pp

echo "Backup completed in $BACKUP_DIR"
ls -la $BACKUP_DIR/
EOF

chmod +x backup_policy.sh
sudo ./backup_policy.sh
Step 2: Test policy removal and restoration

# Test policy removal (be careful!)
echo "Testing policy removal..."
sudo semodule -r mywebapp_custom

# Verify removal
semodule -l | grep mywebapp

# Test application without policy
echo "Testing application without custom policy..."
sudo -u apache python3 /opt/mywebapp/webapp.py 2>&1 | head -5

# Restore policy
echo "Restoring policy..."
sudo semodule -i mywebapp_custom.pp

# Verify restoration
semodule -l | grep mywebapp

# Restore contexts
sudo restorecon -Rv /opt/mywebapp/
