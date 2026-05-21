Lab 71: Installing MySQL Server

Objectives

By the end of this lab, you will be able to:

Install MySQL Server on a Linux system
Configure MySQL to run as a service
Automate MySQL installation and secure configuration using a bash script
Apply basic security best practices for MySQL
Prerequisites

A Linux system (Ubuntu 20.04/Debian or CentOS 8 used in examples)
sudo or root access
Internet connection for package downloads
Basic familiarity with Linux command line
Task 1: Install MySQL Server on Linux

Subtask 1.1: Update System Packages

sudo apt update && sudo apt upgrade -y  # For Debian/Ubuntu
# OR
sudo dnf update -y  # For CentOS/RHEL
Expected Outcome: System packages are updated without errors.

Subtask 1.2: Install MySQL Server

For Debian/Ubuntu:

sudo apt install mysql-server -y
For CentOS/RHEL:

sudo dnf install mysql-server -y
Expected Outcome: MySQL server package is installed successfully.

Subtask 1.3: Verify Installation

mysql --version
Expected Outcome: Output shows MySQL version (e.g., "mysql Ver 8.0.33")

Task 2: Configure MySQL as a Service

Subtask 2.1: Start MySQL Service

sudo systemctl start mysqld  # On CentOS/RHEL
# OR
sudo systemctl start mysql  # On Debian/Ubuntu
Subtask 2.2: Enable Automatic Startup

sudo systemctl enable mysqld  # On CentOS/RHEL
# OR
sudo systemctl enable mysql  # On Debian/Ubuntu
Subtask 2.3: Check Service Status

sudo systemctl status mysqld  # On CentOS/RHEL
# OR
sudo systemctl status mysql  # On Debian/Ubuntu
Expected Outcome: Service shows as "active (running)" and "enabled"

Task 3: Automate Installation with Secure Settings

Subtask 3.1: Create Installation Script

Create mysql_auto_install.sh with the following content:

#!/bin/bash

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

# Detect distribution
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "Cannot detect OS"
    exit 1
fi

# Install MySQL based on OS
case $OS in
    ubuntu|debian)
        apt update
        apt install -y mysql-server
        systemctl start mysql
        systemctl enable mysql
        ;;
    centos|rhel)
        dnf install -y mysql-server
        systemctl start mysqld
        systemctl enable mysqld
        ;;
    *)
        echo "Unsupported OS"
        exit 1
        ;;
esac

# Run MySQL secure installation
echo "Running MySQL secure installation..."
mysql_secure_installation <<EOF
y
0
MySecurePassword123!
y
y
y
y
y
EOF

echo "MySQL installation and configuration complete!"
Subtask 3.2: Make Script Executable

chmod +x mysql_auto_install.sh
Subtask 3.3: Run the Script

sudo ./mysql_auto_install.sh
Expected Outcome:

MySQL is installed and running
Secure configuration is applied (root password set, anonymous users removed, etc.)
Test database removed
Remote root login disabled
Subtask 3.4: Verify Secure Installation

mysql -u root -p
# Enter the password you set in the script
Expected Outcome: You can log in to MySQL shell with the password you configured.

