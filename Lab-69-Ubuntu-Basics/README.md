Lab 69: SSL Certificates in a Real-world Scenario

Objectives

By the end of this lab, you will be able to:

Understand the process of Certificate Authorities (CAs) and SSL/TLS certificates.
Generate a free SSL certificate using Let's Encrypt.
Configure Apache to use the SSL certificate.
Automate SSL certificate installation using a Bash script.
Prerequisites

A Linux-based system (Ubuntu 20.04/22.04 recommended).
Apache web server installed (sudo apt install apache2).
Root or sudo privileges.
A registered domain name pointing to your server's public IP.
Ports 80 (HTTP) and 443 (HTTPS) open in the firewall.
Task 1: Research How to Obtain SSL Certificates from a CA

Subtask 1.1: Understand Certificate Authorities (CAs)

CAs are trusted entities that issue digital certificates to verify the identity of websites.
Popular CAs: Let's Encrypt, DigiCert, Comodo, GlobalSign.
Let's Encrypt is free and open-source, making it ideal for this lab.
Subtask 1.2: Types of SSL Certificates

Single Domain: Covers one domain (e.g., example.com).
Wildcard: Covers a domain and its subdomains (e.g., *.example.com).
Multi-Domain (SAN): Covers multiple domains with one certificate.
Expected Outcome:
Understand the role of CAs and types of SSL certificates.

Task 2: Use Let's Encrypt to Generate a Free SSL Certificate

Subtask 2.1: Install Certbot

Certbot is a tool to automate SSL certificate issuance from Let's Encrypt.

sudo apt update
sudo apt install certbot python3-certbot-apache -y
Subtask 2.2: Obtain the SSL Certificate

Run Certbot to generate a certificate for your domain (example.com):

sudo certbot --apache -d example.com -d www.example.com
Replace example.com with your domain.
Follow the prompts to agree to terms and opt-in for email notifications.
Expected Outcome:
A success message confirming certificate issuance. Certificates are stored in /etc/letsencrypt/live/example.com/.

Troubleshooting Tips:

Ensure your domain resolves to the server's IP.
Check Apache is running (sudo systemctl status apache2).
Task 3: Configure Apache to Use the SSL Certificate

Subtask 3.1: Verify Apache SSL Module

Ensure the SSL module is enabled:

sudo a2enmod ssl
sudo systemctl restart apache2
Subtask 3.2: Update Apache Configuration

Certbot automatically configures Apache, but verify the settings:

sudo nano /etc/apache2/sites-available/example.com-le-ssl.conf
Look for:

<VirtualHost *:443>
    ServerName example.com
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/example.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem
</VirtualHost>
Subtask 3.3: Force HTTPS Redirect

Edit the HTTP configuration to redirect to HTTPS:

sudo nano /etc/apache2/sites-available/example.com.conf
Add:

<VirtualHost *:80>
    ServerName example.com
    Redirect permanent / https://example.com/
</VirtualHost>
Restart Apache:

sudo systemctl restart apache2
Expected Outcome:
Visiting http://example.com redirects to https://example.com with a valid SSL padlock.

Task 4: Write a Script to Automate SSL Certificate Installation

Subtask 4.1: Create a Bash Script

Create ssl_auto_renew.sh to automate renewal:

#!/bin/bash

# Renew SSL certificate
certbot renew --quiet --post-hook "systemctl reload apache2"

# Log renewal status
echo "SSL certificate renewed on $(date)" >> /var/log/ssl_renewal.log
Subtask 4.2: Make the Script Executable

chmod +x ssl_auto_renew.sh
Subtask 4.3: Schedule a Cron Job

Open crontab:

sudo crontab -e
Add (runs daily at midnight):

0 0 * * * /path/to/ssl_auto_renew.sh
Expected Outcome:
The script automatically renews certificates before expiration and reloads Apache.

