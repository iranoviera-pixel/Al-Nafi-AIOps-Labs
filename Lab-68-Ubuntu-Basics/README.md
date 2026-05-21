Lab 68: Configuring Apache with SSL

Objectives

By the end of this lab, you will be able to:

Install and enable SSL modules for Apache.
Generate a self-signed SSL certificate using OpenSSL.
Configure Apache to serve content securely over HTTPS.
Automate SSL certificate renewal with a script.
Prerequisites

A Linux system (Ubuntu/Debian/CentOS)
Sudo or root access
Basic familiarity with the command line
Apache HTTP Server installed (apache2 for Debian/Ubuntu, httpd for CentOS)
OpenSSL installed (usually pre-installed on most Linux distributions)
Task 1: Install SSL Modules for Apache

Step 1.1: Check Apache Installation

Verify Apache is installed and running:

sudo systemctl status apache2   # For Debian/Ubuntu
sudo systemctl status httpd     # For CentOS
Expected Output: Active (running) status.

Step 1.2: Enable SSL Module

Enable the ssl and headers modules for Apache:

sudo a2enmod ssl               # Debian/Ubuntu
sudo a2enmod headers           # Debian/Ubuntu
For CentOS:

sudo yum install mod_ssl       # Install mod_ssl if not present
sudo systemctl restart httpd
Step 1.3: Restart Apache

Apply changes:

sudo systemctl restart apache2   # Debian/Ubuntu
sudo systemctl restart httpd     # CentOS
Troubleshooting Tip: If Apache fails to restart, check logs:

sudo tail -n 20 /var/log/apache2/error.log   # Debian/Ubuntu
sudo tail -n 20 /var/log/httpd/error_log     # CentOS
Task 2: Generate a Self-Signed SSL Certificate

Step 2.1: Create SSL Directory

Create a directory to store certificates:

sudo mkdir /etc/apache2/ssl   # Debian/Ubuntu
sudo mkdir /etc/httpd/ssl     # CentOS
Step 2.2: Generate Certificate

Use OpenSSL to generate a self-signed certificate (valid for 365 days):

sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout /etc/apache2/ssl/apache.key \
-out /etc/apache2/ssl/apache.crt
Explanation:

-x509: Creates a self-signed certificate.
-nodes: Skips passphrase protection (for lab purposes).
-days 365: Sets validity period.
-newkey rsa:2048: Generates a 2048-bit RSA key.
Expected Output: Files /etc/apache2/ssl/apache.key (private key) and /etc/apache2/ssl/apache.crt (certificate).

Task 3: Configure Apache to Use SSL

Step 3.1: Create SSL Configuration File

Edit or create a virtual host file for HTTPS:

sudo nano /etc/apache2/sites-available/default-ssl.conf   # Debian/Ubuntu
sudo nano /etc/httpd/conf.d/ssl.conf                      # CentOS
Add the following configuration (adjust paths for CentOS):

<VirtualHost *:443>
    ServerAdmin admin@example.com
    ServerName your_domain_or_IP

    SSLEngine on
    SSLCertificateFile /etc/apache2/ssl/apache.crt
    SSLCertificateKeyFile /etc/apache2/ssl/apache.key

    DocumentRoot /var/www/html
    ErrorLog ${APACHE_LOG_DIR}/error.log
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
Step 3.2: Enable SSL Site

Enable the SSL site and restart Apache:

sudo a2ensite default-ssl.conf   # Debian/Ubuntu
sudo systemctl restart apache2
For CentOS:

sudo systemctl restart httpd
Step 3.3: Test HTTPS Access

Open a browser and navigate to https://your_server_ip. Accept the security warning (self-signed certificate).

Troubleshooting Tip: If the page doesn’t load, check firewall settings:

sudo ufw allow 443   # Debian/Ubuntu
sudo firewall-cmd --add-service=https --permanent && sudo firewall-cmd --reload   # CentOS
Task 4: Automate SSL Certificate Renewal

Step 4.1: Create Renewal Script

Create a script (/usr/local/bin/renew_ssl.sh) to regenerate the certificate:

#!/bin/bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout /etc/apache2/ssl/apache.key \
-out /etc/apache2/ssl/apache.crt -subj "/CN=your_domain_or_IP"
sudo systemctl restart apache2
Make the script executable:

sudo chmod +x /usr/local/bin/renew_ssl.sh
Step 4.2: Schedule with Cron

Edit the crontab to run the script annually:

sudo crontab -e
Add this line (runs at midnight on Jan 1):

0 0 1 1 * /usr/local/bin/renew_ssl.sh

