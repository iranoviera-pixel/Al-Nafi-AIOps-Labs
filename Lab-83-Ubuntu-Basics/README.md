Lab 83: Installing Pnp4Nagios

Objectives

By the end of this lab, you will be able to:

Install Pnp4Nagios on a Nagios server.
Configure Nagios to send performance data to Pnp4Nagios.
Automate the installation and integration process using a Bash script.
Prerequisites

A Linux-based Nagios server (Ubuntu/CentOS)
Root or sudo privileges
Basic familiarity with Nagios configuration
Internet access for package downloads
Task 1: Install Pnp4Nagios on the Nagios Server

Subtask 1.1: Install Dependencies

Pnp4Nagios requires the following dependencies:

Apache/Nginx (web server)
PHP
RRDtool (for graph generation)
For Ubuntu/Debian:

sudo apt update
sudo apt install -y apache2 php libapache2-mod-php rrdtool
For CentOS/RHEL:

sudo yum install -y httpd php rrdtool
Expected Outcome:
All dependencies are installed without errors.

Subtask 1.2: Download and Install Pnp4Nagios

Download the latest stable release from the official repository:

wget https://github.com/lingej/pnp4nagios/archive/refs/tags/v0.6.26.tar.gz
tar xzf v0.6.26.tar.gz
cd pnp4nagios-0.6.26
Compile and install:

./configure --with-nagios-user=nagios --with-nagios-group=nagios
make all
sudo make install
sudo make install-webconf
sudo make install-config
sudo make install-init
Expected Outcome:
Pnp4Nagios is installed in /usr/local/pnp4nagios.

Subtask 1.3: Configure Apache/Nginx

Enable the Apache configuration and restart the service:

sudo a2enmod rewrite
sudo systemctl restart apache2
For CentOS:

sudo systemctl enable httpd
sudo systemctl restart httpd
Expected Outcome:
Pnp4Nagios web interface is accessible at http://<your-server-ip>/pnp4nagios.

Task 2: Configure Nagios to Send Data to Pnp4Nagios

Subtask 2.1: Enable Performance Data Processing

Edit the Nagios main configuration file:

sudo nano /usr/local/nagios/etc/nagios.cfg
Uncomment or add these lines:

process_performance_data=1
host_perfdata_command=process-host-perfdata
service_perfdata_command=process-service-perfdata
Expected Outcome:
Nagios is configured to process performance data.

Subtask 2.2: Define Performance Data Commands

Add the following to /usr/local/nagios/etc/objects/commands.cfg:

define command {
    command_name    process-host-perfdata
    command_line    /usr/local/pnp4nagios/libexec/process_perfdata.pl -d HOSTPERFDATA
}

define command {
    command_name    process-service-perfdata
    command_line    /usr/local/pnp4nagios/libexec/process_perfdata.pl -d SERVICEPERFDATA
}
Expected Outcome:
Nagios can now forward performance data to Pnp4Nagios.

Subtask 2.3: Restart Nagios

Apply the configuration:

sudo systemctl restart nagios
Expected Outcome:
Performance data appears in Pnp4Nagios web interface.

Task 3: Automate Pnp4Nagios Installation and Integration

Subtask 3.1: Create an Installation Script

Save the following as install_pnp4nagios.sh:

#!/bin/bash

# Install dependencies
if [ -f /etc/redhat-release ]; then
    sudo yum install -y httpd php rrdtool
else
    sudo apt update
    sudo apt install -y apache2 php libapache2-mod-php rrdtool
fi

# Download and install Pnp4Nagios
wget https://github.com/lingej/pnp4nagios/archive/refs/tags/v0.6.26.tar.gz
tar xzf v0.6.26.tar.gz
cd pnp4nagios-0.6.26
./configure --with-nagios-user=nagios --with-nagios-group=nagios
make all
sudo make install
sudo make install-webconf
sudo make install-config
sudo make install-init

# Configure Apache
if [ -f /etc/redhat-release ]; then
    sudo systemctl enable httpd
    sudo systemctl restart httpd
else
    sudo a2enmod rewrite
    sudo systemctl restart apache2
fi

# Configure Nagios
sudo sed -i 's/^process_performance_data=.*/process_performance_data=1/' /usr/local/nagios/etc/nagios.cfg
sudo sed -i 's/^#host_perfdata_command=.*/host_perfdata_command=process-host-perfdata/' /usr/local/nagios/etc/nagios.cfg
sudo sed -i 's/^#service_perfdata_command=.*/service_perfdata_command=process-service-perfdata/' /usr/local/nagios/etc/nagios.cfg

# Add commands to commands.cfg
echo 'define command {
    command_name    process-host-perfdata
    command_line    /usr/local/pnp4nagios/libexec/process_perfdata.pl -d HOSTPERFDATA
}' | sudo tee -a /usr/local/nagios/etc/objects/commands.cfg

echo 'define command {
    command_name    process-service-perfdata
    command_line    /usr/local/pnp4nagios/libexec/process_perfdata.pl -d SERVICEPERFDATA
}' | sudo tee -a /usr/local/nagios/etc/objects/commands.cfg

# Restart Nagios
sudo systemctl restart nagios

echo "Pnp4Nagios installation and configuration complete!"
Make it executable:

chmod +x install_pnp4nagios.sh
Expected Outcome:
Running the script automates the entire installation and configuration process.


