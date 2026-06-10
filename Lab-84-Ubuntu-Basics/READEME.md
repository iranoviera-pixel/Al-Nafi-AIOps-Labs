Lab 84: Installing NRPE Agent

Objectives

By the end of this lab, you will be able to:

Install and configure the NRPE (Nagios Remote Plugin Executor) agent on a Linux client.
Set up the Nagios server to monitor the client using NRPE.
Automate NRPE installation and configuration using a shell script.
Prerequisites

A Linux client machine (Ubuntu/CentOS)
A Nagios server already set up
SSH access to the client machine
Sudo privileges on both machines
Basic knowledge of Linux commands and Nagios configuration
Task 1: Install the NRPE Agent on a Linux Client

Subtask 1.1: Update the System

Before installing NRPE, ensure the system is up-to-date.

For Ubuntu/Debian:

sudo apt update && sudo apt upgrade -y
For CentOS/RHEL:

sudo yum update -y
Expected Outcome: The system packages are updated.

Subtask 1.2: Install Required Dependencies

NRPE requires nagios-plugins and NRPE packages.

For Ubuntu/Debian:

sudo apt install -y nagios-plugins nagios-nrpe-server
For CentOS/RHEL:

sudo yum install -y epel-release
sudo yum install -y nrpe nagios-plugins-all
Expected Outcome: NRPE and Nagios plugins are installed.

Subtask 1.3: Configure NRPE on the Client

Edit the NRPE configuration file to allow the Nagios server to connect.

Open the NRPE config file:

sudo nano /etc/nagios/nrpe.cfg
Find and modify the following lines:

allowed_hosts=127.0.0.1,<NAGIOS_SERVER_IP>
dont_blame_nrpe=1
Replace <NAGIOS_SERVER_IP> with your Nagios server's IP.

Save and exit (Ctrl+O, Enter, Ctrl+X).

Expected Outcome: NRPE is configured to accept connections from the Nagios server.

Subtask 1.4: Start and Enable NRPE Service

Start the NRPE service and enable it to run at boot.

For Ubuntu/Debian:

sudo systemctl start nagios-nrpe-server
sudo systemctl enable nagios-nrpe-server
For CentOS/RHEL:

sudo systemctl start nrpe
sudo systemctl enable nrpe
Verify the service is running:

sudo systemctl status nrpe  # or nagios-nrpe-server
Expected Outcome: NRPE service is active and running.

Task 2: Configure Nagios Server to Monitor the Client Using NRPE

Subtask 2.1: Add Client Definition on Nagios Server

On the Nagios server, create a new configuration file for the client:

sudo nano /usr/local/nagios/etc/servers/client.cfg
Add the following configuration (replace <CLIENT_IP> with the client's IP):

define host {
    use                     linux-server
    host_name               nrpe-client
    alias                   NRPE Client
    address                 <CLIENT_IP>
}

define service {
    use                     generic-service
    host_name               nrpe-client
    service_description     CPU Load
    check_command           check_nrpe!check_load
}

define service {
    use                     generic-service
    host_name               nrpe-client
    service_description     Disk Usage
    check_command           check_nrpe!check_disk
}
Save and exit.

Expected Outcome: Nagios server is configured to monitor the client.

Subtask 2.2: Restart Nagios Service

Apply the changes by restarting Nagios:

sudo systemctl restart nagios
Verify the configuration:

sudo /usr/local/nagios/bin/nagios -v /usr/local/nagios/etc/nagios.cfg
Expected Outcome: No errors in the validation, and the client appears in the Nagios web interface.

Task 3: Automate NRPE Installation and Configuration

Subtask 3.1: Write an Installation Script

Create a script (install_nrpe.sh) to automate NRPE installation on remote systems.

#!/bin/bash

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "Please run as root."
    exit 1
fi

# Detect OS and install NRPE
if [ -f /etc/os-release ]; then
    . /etc/os-release
    case $ID in
        ubuntu|debian)
            apt update && apt install -y nagios-plugins nagios-nrpe-server
            sed -i "s/allowed_hosts=127.0.0.1/allowed_hosts=127.0.0.1,<NAGIOS_SERVER_IP>/" /etc/nagios/nrpe.cfg
            systemctl start nagios-nrpe-server
            systemctl enable nagios-nrpe-server
            ;;
        centos|rhel)
            yum install -y epel-release
            yum install -y nrpe nagios-plugins-all
            sed -i "s/allowed_hosts=127.0.0.1/allowed_hosts=127.0.0.1,<NAGIOS_SERVER_IP>/" /etc/nagios/nrpe.cfg
            systemctl start nrpe
            systemctl enable nrpe
            ;;
        *)
            echo "Unsupported OS."
            exit 1
            ;;
    esac
else
    echo "Cannot detect OS."
    exit 1
fi

echo "NRPE installation and configuration completed."
Replace <NAGIOS_SERVER_IP> with your Nagios server's IP.

Subtask 3.2: Run the Script on Remote Systems

Use scp and ssh to deploy the script to a remote client and execute it.

Copy the script to the client:

scp install_nrpe.sh user@client_ip:/tmp/
Execute the script on the client:

ssh user@client_ip "sudo bash /tmp/install_nrpe.sh"
Expected Outcome: NRPE is automatically installed and configured on the remote client.
