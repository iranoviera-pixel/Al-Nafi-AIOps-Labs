Lab 86: Adding a Linux Client to Nagios

Objectives

By the end of this lab, you will be able to:

Configure Nagios to monitor a remote Linux client using NRPE (Nagios Remote Plugin Executor).
Automate the process of new Linux client additions to Nagios using a Bash script.
Validate the monitoring setup by executing Nagios checks on the client system.
Prerequisites

A working Nagios server (version 4.x or later) installed on a Linux system.
A remote Linux client (Ubuntu/CentOS) with SSH access.
Basic knowledge of Linux command line and Nagios configuration files.
sudo privileges on both systems.
Task 1: Configure Nagios to Monitor a Remote Linux Client Using NRPE

Subtask 1.1: Install NRPE and Nagios Plugins on the Client

Connect to the Linux client via SSH:

ssh username@client_ip
Install NRPE and Nagios plugins:

For Ubuntu/Debian:
sudo apt update
sudo apt install -y nagios-nrpe-server nagios-plugins
For CentOS/RHEL:
sudo yum install -y epel-release
sudo yum install -y nrpe nagios-plugins-all
Verify the installation:

nrpe --version
Subtask 1.2: Configure NRPE on the Client

Edit the NRPE configuration file:

sudo nano /etc/nagios/nrpe.cfg
Update the allowed_hosts directive to include the Nagios server IP:

allowed_hosts=127.0.0.1,<nagios_server_ip>
Restart the NRPE service:

sudo systemctl restart nrpe
Subtask 1.3: Add the Client to Nagios Server

On the Nagios server, create a new host configuration file:

sudo nano /usr/local/nagios/etc/objects/linux_client.cfg
Add the following configuration (replace placeholders):

define host {
    use                     linux-server
    host_name               linux_client
    alias                   Linux Client
    address                 <client_ip>
}

define service {
    use                     generic-service
    host_name               linux_client
    service_description     PING
    check_command           check_ping!100.0,20%!500.0,60%
}

define service {
    use                     generic-service
    host_name               linux_client
    service_description     Disk Usage
    check_command           check_nrpe!check_disk
}
Restart Nagios to apply changes:

sudo systemctl restart nagios
Task 2: Automate Client Addition with a Bash Script

Subtask 2.1: Create the Automation Script

On the Nagios server, create a script:

sudo nano /usr/local/bin/add_nagios_client.sh
Add the following script (replace placeholders):

#!/bin/bash
# Usage: ./add_nagios_client.sh <client_ip> <client_name>

CLIENT_IP=$1
CLIENT_NAME=$2
CONFIG_FILE="/usr/local/nagios/etc/objects/${CLIENT_NAME}.cfg"

# Create host configuration
echo "define host {
    use                     linux-server
    host_name               ${CLIENT_NAME}
    alias                   ${CLIENT_NAME}
    address                 ${CLIENT_IP}
}" > $CONFIG_FILE

# Add default services
echo "define service {
    use                     generic-service
    host_name               ${CLIENT_NAME}
    service_description     PING
    check_command           check_ping!100.0,20%!500.0,60%
}" >> $CONFIG_FILE

echo "Client ${CLIENT_NAME} added successfully. Restart Nagios to apply changes."
Make the script executable:

sudo chmod +x /usr/local/bin/add_nagios_client.sh
Subtask 2.2: Test the Script

Run the script:

sudo ./add_nagios_client.sh <client_ip> linux_client_2
Restart Nagios:

sudo systemctl restart nagios
Task 3: Test Nagios Checks on the Client

Subtask 3.1: Verify NRPE Connectivity

On the Nagios server, test NRPE connection:

/usr/lib/nagios/plugins/check_nrpe -H <client_ip>
Expected Output: NRPE version number.
Test a remote command:

/usr/lib/nagios/plugins/check_nrpe -H <client_ip> -c check_load
Subtask 3.2: Validate in Nagios Web Interface

Access the Nagios web UI (http://<nagios_server_ip>/nagios).
Navigate to Hosts and verify the new client appears.
Check service statuses under Services.

