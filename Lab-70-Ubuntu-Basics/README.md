Lab 70: Configuring Virtual Hosts on Apache

Objectives

By the end of this lab, you will be able to:

Understand the concept of Apache Virtual Hosts
Configure multiple virtual hosts on an Apache web server
Set up distinct websites with unique domain names
Automate virtual host creation using a Bash script
Prerequisites

A Linux-based system (Ubuntu/Debian/CentOS)
Apache web server installed (sudo apt install apache2 for Ubuntu/Debian or sudo yum install httpd for CentOS)
Basic understanding of Linux command line
Root or sudo privileges
A text editor (nano, vim, etc.)
Task 1: Create Multiple Virtual Host Configurations in Apache

Subtask 1.1: Create Directory Structure for Virtual Hosts

Create directories for two sample websites:

sudo mkdir -p /var/www/site1/public_html
sudo mkdir -p /var/www/site2/public_html
Set proper permissions:

sudo chown -R $USER:$USER /var/www/site1/public_html
sudo chown -R $USER:$USER /var/www/site2/public_html
sudo chmod -R 755 /var/www
Expected Outcome: Directories /var/www/site1/public_html and /var/www/site2/public_html are created with correct permissions.

Subtask 1.2: Create Sample Index Pages

Create a sample index.html for site1:

echo "<h1>Welcome to Site 1</h1>" > /var/www/site1/public_html/index.html
Create a sample index.html for site2:

echo "<h1>Welcome to Site 2</h1>" > /var/www/site2/public_html/index.html
Expected Outcome: Basic HTML files are created for both websites.

Subtask 1.3: Create Virtual Host Configuration Files

Create a configuration file for site1:

sudo nano /etc/apache2/sites-available/site1.conf
Add the following content (for Ubuntu/Debian):

<VirtualHost *:80>
    ServerAdmin admin@site1.local
    ServerName site1.local
    ServerAlias www.site1.local
    DocumentRoot /var/www/site1/public_html
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
Repeat for site2:

sudo nano /etc/apache2/sites-available/site2.conf
<VirtualHost *:80>
    ServerAdmin admin@site2.local
    ServerName site2.local
    ServerAlias www.site2.local
    DocumentRoot /var/www/site2/public_html
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
Expected Outcome: Virtual host configuration files are created for both sites.

Subtask 1.4: Enable the Virtual Hosts

Enable the sites:

sudo a2ensite site1.conf
sudo a2ensite site2.conf
Disable the default site (optional):

sudo a2dissite 000-default.conf
Restart Apache:

sudo systemctl restart apache2
Expected Outcome: Virtual hosts are enabled, and Apache restarts without errors.

Task 2: Set Up Different Websites with Unique Domain Names

Subtask 2.1: Update Local Hosts File

Edit the /etc/hosts file to map domain names to localhost:

sudo nano /etc/hosts
Add these lines:

127.0.0.1   site1.local
127.0.0.1   site2.local
Expected Outcome: Domain names resolve to the local machine.

Subtask 2.2: Test the Virtual Hosts

Open a web browser and visit:

http://site1.local
http://site2.local
Alternatively, use curl:

curl http://site1.local
curl http://site2.local
Expected Outcome: You see "Welcome to Site 1" and "Welcome to Site 2" respectively.

Task 3: Automate Virtual Host Creation with a Script

Subtask 3.1: Create a Bash Script

Create a script file:

nano create_vhost.sh
Add the following script:

#!/bin/bash

# Check if domain name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 domain_name"
    exit 1
fi

DOMAIN=$1
SITE_DIR="/var/www/$DOMAIN/public_html"
CONF_FILE="/etc/apache2/sites-available/$DOMAIN.conf"

# Create directory structure
sudo mkdir -p $SITE_DIR
sudo chown -R $USER:$USER $SITE_DIR
sudo chmod -R 755 /var/www

# Create sample index page
echo "<h1>Welcome to $DOMAIN</h1>" > "$SITE_DIR/index.html"

# Create virtual host config
sudo bash -c "cat > $CONF_FILE <<EOF
<VirtualHost *:80>
    ServerAdmin admin@$DOMAIN
    ServerName $DOMAIN
    ServerAlias www.$DOMAIN
    DocumentRoot $SITE_DIR
    ErrorLog \${APACHE_LOG_DIR}/error.log
    CustomLog \${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
EOF"

# Enable site and restart Apache
sudo a2ensite $DOMAIN.conf
sudo systemctl restart apache2

# Update hosts file
sudo sh -c "echo '127.0.0.1   $DOMAIN' >> /etc/hosts"
sudo sh -c "echo '127.0.0.1   www.$DOMAIN' >> /etc/hosts"

echo "Virtual host for $DOMAIN created successfully!"
Make the script executable:

chmod +x create_vhost.sh
Subtask 3.2: Test the Script

Run the script to create a new virtual host:

./create_vhost.sh newsite.local
Verify the new site:

curl http://newsite.local
Expected Outcome: The script creates a new virtual host, and you see "Welcome to newsite.local".

