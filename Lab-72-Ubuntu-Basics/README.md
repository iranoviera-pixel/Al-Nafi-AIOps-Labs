Lab 72: Managing MySQL Databases with PhpMyAdmin

Objectives

By the end of this lab, you will be able to:

Install PhpMyAdmin on a Linux server
Configure PhpMyAdmin to connect to a MySQL database
Automate PhpMyAdmin installation and configuration using a Bash script
Perform basic database management tasks using PhpMyAdmin
Prerequisites

A Linux server (Ubuntu 20.04/22.04 LTS recommended)
Sudo or root access
LAMP stack installed (Apache, MySQL, PHP)
Basic Linux command line knowledge
Task 1: Install PhpMyAdmin on the Server

Subtask 1.1: Update System Packages

Before installation, ensure your system packages are up to date.

sudo apt update && sudo apt upgrade -y
Expected Outcome:
All system packages are updated without errors.

Subtask 1.2: Install PhpMyAdmin

Install PhpMyAdmin using the package manager.

sudo apt install phpmyadmin -y
During installation:

Select Apache2 as the web server (use Spacebar to select, then Enter).
Choose Yes when asked to configure the database with dbconfig-common.
Set a password for the PhpMyAdmin database (or leave blank to generate automatically).
Expected Outcome:
PhpMyAdmin is installed and accessible at http://your-server-ip/phpmyadmin.

Troubleshooting Tips:

If you get a "404 Not Found" error, enable the PhpMyAdmin Apache configuration:
sudo ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
sudo a2enconf phpmyadmin
sudo systemctl reload apache2
Task 2: Configure PhpMyAdmin to Connect to MySQL

Subtask 2.1: Secure MySQL Access

Ensure MySQL has a root password set (if not done during installation).

sudo mysql_secure_installation
Follow the prompts to set a root password and secure the installation.

Subtask 2.2: Configure PhpMyAdmin Authentication

Edit the PhpMyAdmin configuration to use MySQL credentials.

sudo nano /etc/phpmyadmin/config.inc.php
Add or modify the following lines:

$cfg['Servers'][$i]['auth_type'] = 'cookie';  // Use cookie-based authentication
$cfg['Servers'][$i]['host'] = 'localhost';    // MySQL host
$cfg['Servers'][$i]['connect_type'] = 'tcp';  // Connection type
Save and exit (Ctrl+O, Enter, Ctrl+X).

Expected Outcome:
PhpMyAdmin will prompt for MySQL credentials when accessed.

Subtask 2.3: Test PhpMyAdmin Access

Open a web browser and navigate to:

http://your-server-ip/phpmyadmin
Log in using your MySQL root credentials.

Expected Outcome:
Successful login to the PhpMyAdmin dashboard.

Task 3: Write a Script to Automate PhpMyAdmin Installation and Configuration

Subtask 3.1: Create an Automation Script

Create a Bash script (install_phpmyadmin.sh) to automate the process.

#!/bin/bash

# Update system
sudo apt update && sudo apt upgrade -y

# Install PhpMyAdmin non-interactively
sudo DEBIAN_FRONTEND=noninteractive apt install -y phpmyadmin

# Configure Apache
sudo ln -s /etc/phpmyadmin/apache.conf /etc/apache2/conf-available/phpmyadmin.conf
sudo a2enconf phpmyadmin
sudo systemctl reload apache2

# Configure PhpMyAdmin
sudo sed -i "s/\$cfg\['Servers'\]\[\$i\]\['auth_type'\] = 'config';/\$cfg\['Servers'\]\[\$i\]\['auth_type'\] = 'cookie';/" /etc/phpmyadmin/config.inc.php

echo "PhpMyAdmin installed and configured. Access at http://$(hostname -I | awk '{print $1}')/phpmyadmin"
Subtask 3.2: Make the Script Executable

chmod +x install_phpmyadmin.sh
Subtask 3.3: Run the Script

sudo ./install_phpmyadmin.sh
Expected Outcome:
PhpMyAdmin is installed and configured without manual intervention.

