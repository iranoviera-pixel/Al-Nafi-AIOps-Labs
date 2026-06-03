Lab 88: Setting Up Docker Containers Monitoring

Objectives

By the end of this lab, you will be able to:

Install and configure Nagios for Docker container monitoring.
Use Nagios plugins to monitor container status and resource usage.
Automate container monitoring configuration in Nagios using a custom script.
Prerequisites

Before starting this lab, ensure you have:

A system running Ubuntu 20.04 LTS or later.
Docker installed and running (sudo docker run hello-world should work).
Basic familiarity with Linux command line and Docker concepts.
sudo privileges on the system.
Task 1: Install and Configure Nagios for Docker Monitoring

Subtask 1.1: Install Nagios Core

Update your system packages:

sudo apt update && sudo apt upgrade -y
Install required dependencies:

sudo apt install -y autoconf gcc libc6 make wget unzip apache2 php libapache2-mod-php libgd-dev libssl-dev
Download and extract Nagios Core:

wget https://github.com/NagiosEnterprises/nagioscore/archive/nagios-4.4.6.tar.gz
tar -xzf nagios-4.4.6.tar.gz
cd nagioscore-nagios-4.4.6/
Compile and install Nagios:

sudo ./configure --with-httpd-conf=/etc/apache2/sites-enabled
sudo make all
sudo make install
sudo make install-init
sudo make install-commandmode
sudo make install-config
sudo make install-webconf
Create a Nagios admin user and set a password:

sudo htpasswd -c /usr/local/nagios/etc/htpasswd.users nagiosadmin
Restart Apache to apply changes:

sudo systemctl restart apache2
Start Nagios and enable it on boot:

sudo systemctl start nagios
sudo systemctl enable nagios
Expected Outcome: Nagios web interface should be accessible at http://<your-server-ip>/nagios. Log in using nagiosadmin and the password you set.

Subtask 1.2: Install Nagios Plugins

Install required dependencies for plugins:

sudo apt install -y autoconf gcc libc6 libmcrypt-dev make libssl-dev wget bc gawk dc build-essential snmp libnet-snmp-perl gettext
Download and install Nagios Plugins:

wget https://github.com/nagios-plugins/nagios-plugins/archive/release-2.3.3.tar.gz
tar -xzf release-2.3.3.tar.gz
cd nagios-plugins-release-2.3.3/
sudo ./tools/setup
sudo ./configure
sudo make
sudo make install
Expected Outcome: Nagios plugins are installed in /usr/local/nagios/libexec/.

Task 2: Monitor Docker Containers Using Nagios Plugins

Subtask 2.1: Install check_docker Plugin

Install Python and required dependencies:

sudo apt install -y python3 python3-pip
pip3 install docker
Download the check_docker plugin:

wget https://raw.githubusercontent.com/timdaman/check_docker/master/check_docker.py -O /usr/local/nagios/libexec/check_docker.py
chmod +x /usr/local/nagios/libexec/check_docker.py
Test the plugin:

/usr/local/nagios/libexec/check_docker.py --list
(Should list running containers.)

Subtask 2.2: Configure Nagios to Monitor Docker

Edit Nagios configuration to define a Docker host:

sudo nano /usr/local/nagios/etc/objects/docker.cfg
Add the following:

define host {
    use             linux-server
    host_name       docker-host
    alias           Docker Host
    address         127.0.0.1
}

define service {
    use                 generic-service
    host_name           docker-host
    service_description Docker Container Status
    check_command       check_docker!--container <container_name> --status
}
Restart Nagios:

sudo systemctl restart nagios
Expected Outcome: Nagios dashboard now shows Docker container status.

Task 3: Automate Container Monitoring with a Script

Subtask 3.1: Write an Automation Script

Create a script to auto-add Docker containers to Nagios:

sudo nano /usr/local/nagios/scripts/add_docker_monitoring.sh
Paste the following:

#!/bin/bash
CONTAINERS=$(docker ps --format "{{.Names}}")
NAGIOS_CFG="/usr/local/nagios/etc/objects/docker.cfg"

echo "# Auto-generated Docker monitoring config" > $NAGIOS_CFG

for container in $CONTAINERS; do
    echo "define service {" >> $NAGIOS_CFG
    echo "    use                 generic-service" >> $NAGIOS_CFG
    echo "    host_name           docker-host" >> $NAGIOS_CFG
    echo "    service_description Docker Container: $container" >> $NAGIOS_CFG
    echo "    check_command       check_docker!--container $container --status" >> $NAGIOS_CFG
    echo "}" >> $NAGIOS_CFG
done

sudo systemctl restart nagios
Make the script executable:

chmod +x /usr/local/nagios/scripts/add_docker_monitoring.sh
Run the script:

sudo /usr/local/nagios/scripts/add_docker_monitoring.sh
Expected Outcome: All running Docker containers are automatically added to Nagios.
