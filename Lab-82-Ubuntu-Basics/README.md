Lab 82: Nagios Installation

Objectives

By the end of this lab, you will be able to:

Install Nagios Core on a Linux system.
Install and configure necessary dependencies for Nagios.
Set up Nagios to monitor local system performance and services.
Automate the installation process using a Bash script.
Prerequisites

A Linux system (Ubuntu 20.04/22.04 or CentOS 7/8 recommended)
Sudo or root privileges
Basic knowledge of Linux commands
Internet access for downloading packages
Task 1: Install Nagios on a Linux System

Subtask 1.1: Update the System

Before installing Nagios, ensure your system is up-to-date.

sudo apt update && sudo apt upgrade -y  # For Ubuntu/Debian
# OR
sudo yum update -y                     # For CentOS/RHEL
Expected Outcome:
All system packages are updated without errors.

Subtask 1.2: Install Required Packages

Install the necessary packages for Nagios compilation and operation.

# For Ubuntu/Debian
sudo apt install -y build-essential apache2 php libapache2-mod-php \
    libgd-dev libssl-dev libapache2-mod-php openssl perl \
    unzip wget make

# For CentOS/RHEL
sudo yum install -y httpd php gcc glibc glibc-common gd gd-devel \
    make net-snmp openssl-devel wget unzip
Expected Outcome:
All dependencies are installed successfully.

Subtask 1.3: Download and Install Nagios Core

Download the latest Nagios Core source code and compile it.

# Download Nagios Core
wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.4.6.tar.gz
tar -xzf nagios-*.tar.gz
cd nagios-4.4.6

# Compile and install
./configure --with-httpd-conf=/etc/apache2/sites-enabled  # For Ubuntu/Debian
# OR
./configure --with-httpd-conf=/etc/httpd/conf.d           # For CentOS/RHEL

make all
sudo make install
sudo make install-commandmode
sudo make install-config
sudo make install-webconf
Expected Outcome:
Nagios Core is installed in /usr/local/nagios.

Subtask 1.4: Create Nagios User and Set Permissions

Create a dedicated Nagios user and configure Apache permissions.

sudo useradd nagios
sudo usermod -aG nagios www-data  # Ubuntu/Debian
# OR
sudo usermod -aG nagios apache    # CentOS/RHEL

sudo chown -R nagios:nagios /usr/local/nagios
Expected Outcome:
Permissions are correctly set for the Nagios directory.

Task 2: Install Nagios Plugins and NRPE

Subtask 2.1: Install Nagios Plugins

Nagios plugins allow monitoring of various services.

wget https://nagios-plugins.org/download/nagios-plugins-2.3.3.tar.gz
tar -xzf nagios-plugins-*.tar.gz
cd nagios-plugins-2.3.3

./configure --with-nagios-user=nagios --with-nagios-group=nagios
make
sudo make install
Expected Outcome:
Plugins are installed in /usr/local/nagios/libexec.

Subtask 2.2: Install NRPE (Nagios Remote Plugin Executor)

NRPE allows remote monitoring.

wget https://github.com/NagiosEnterprises/nrpe/releases/download/nrpe-4.1.0/nrpe-4.1.0.tar.gz
tar -xzf nrpe-*.tar.gz
cd nrpe-4.1.0

./configure
make all
sudo make install
sudo make install-config
sudo make install-init
Expected Outcome:
NRPE is installed and configured.

Task 3: Configure Nagios for Local Monitoring

Subtask 3.1: Configure Apache for Nagios Web Interface

Enable the Apache configuration and restart the service.

# For Ubuntu/Debian
sudo a2enmod cgi
sudo systemctl restart apache2

# For CentOS/RHEL
sudo systemctl enable httpd
sudo systemctl restart httpd
Expected Outcome:
Apache serves the Nagios web interface at http://<your-server-ip>/nagios.

Subtask 3.2: Set Up Nagios Admin Password

Create a password for the Nagios web interface.

sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin
Expected Outcome:
A login prompt appears when accessing the Nagios web interface.

Subtask 3.3: Define a Local Host in Nagios

Edit the Nagios configuration to monitor the localhost.

sudo nano /usr/local/nagios/etc/objects/localhost.cfg
Add the following host definition:

define host {
    use                     linux-server
    host_name               localhost
    alias                   Local Server
    address                 127.0.0.1
}

define service {
    use                     generic-service
    host_name               localhost
    service_description     CPU Load
    check_command           check_nrpe!check_load
}

define service {
    use                     generic-service
    host_name               localhost
    service_description     Disk Usage
    check_command           check_nrpe!check_disk
}
Expected Outcome:
Nagios monitors CPU load and disk usage of the local system.

Subtask 3.4: Start Nagios Service

Enable and start Nagios.

sudo systemctl enable nagios
sudo systemctl start nagios
Expected Outcome:
Nagios runs and monitors the defined services.

Task 4: Automate Nagios Installation with a Script

Subtask 4.1: Write a Bash Script for Installation

Create an automation script (install_nagios.sh):

#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install dependencies
sudo apt install -y build-essential apache2 php libapache2-mod-php \
    libgd-dev libssl-dev libapache2-mod-php openssl perl unzip wget make

# Download and install Nagios Core
wget https://assets.nagios.com/downloads/nagioscore/releases/nagios-4.4.6.tar.gz
tar -xzf nagios-*.tar.gz
cd nagios-4.4.6
./configure --with-httpd-conf=/etc/apache2/sites-enabled
make all
sudo make install
sudo make install-commandmode
sudo make install-config
sudo make install-webconf

# Set up Nagios user
sudo useradd nagios
sudo usermod -aG nagios www-data
sudo chown -R nagios:nagios /usr/local/nagios

# Install Nagios plugins
wget https://nagios-plugins.org/download/nagios-plugins-2.3.3.tar.gz
tar -xzf nagios-plugins-*.tar.gz
cd nagios-plugins-2.3.3
./configure --with-nagios-user=nagios --with-nagios-group=nagios
make
sudo make install

# Configure Apache and start services
sudo a2enmod cgi
sudo systemctl restart apache2
sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin
sudo systemctl enable nagios
sudo systemctl start nagios

echo "Nagios installation completed! Access at http://$(hostname -I | awk '{print $1}')/nagios"
Expected Outcome:
Running the script automates the entire Nagios installation.
