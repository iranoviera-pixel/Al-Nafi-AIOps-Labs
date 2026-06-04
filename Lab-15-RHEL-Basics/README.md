Lab 15: Centralized Authentication with SSSD/LDAP

Objectives

By the end of this lab, students will be able to:

Understand the basics of centralized authentication using SSSD and LDAP.
Install and configure SSSD to connect to an LDAP server.
Automate SSSD/LDAP configuration and user synchronization using a script.
Test and verify centralized authentication.
Prerequisites

Before starting this lab, students should have:

Basic familiarity with Linux command line.
A Linux-based system (provided by Al Nafi's cloud machines—just click Start Lab).
Sudo or root access to the machine.
An active internet connection to install packages.
Task 1: Install and Configure SSSD and LDAP

Step 1: Install Required Packages

Open a terminal on your Linux machine.
Run the following command to update your package list:
sudo apt update
Install SSSD and LDAP client packages:
sudo apt install -y sssd ldap-utils
Expected Outcome: Packages are installed without errors.
Step 2: Configure LDAP Server Connection

Edit the SSSD configuration file:
sudo nano /etc/sssd/sssd.conf
Add the following configuration (replace ldap.example.com with your LDAP server address):
[sssd]
config_file_version = 2
services = nss, pam
domains = default

[domain/default]
id_provider = ldap
auth_provider = ldap
ldap_uri = ldap://ldap.example.com
ldap_search_base = dc=example,dc=com
ldap_user_search_base = ou=users,dc=example,dc=com
ldap_group_search_base = ou=groups,dc=example,dc=com
cache_credentials = True
Save the file (Ctrl+O, then Ctrl+X).
Step 3: Set Permissions and Restart SSSD

Set strict permissions for the SSSD config file:
sudo chmod 600 /etc/sssd/sssd.conf
Restart the SSSD service:
sudo systemctl restart sssd
Expected Outcome: SSSD starts without errors.
Task 2: Test LDAP Authentication

Step 1: Verify LDAP Connectivity

Test LDAP search using ldapsearch:
ldapsearch -x -H ldap://ldap.example.com -b "dc=example,dc=com"
Expected Outcome: A list of LDAP entries is displayed.
Step 2: Test User Authentication

Use getent to check if LDAP users are visible:
getent passwd
Expected Outcome: LDAP users appear in the output.
Task 3: Automate SSSD/LDAP Configuration

Step 1: Create a Configuration Script

Create a script named configure_sssd_ldap.sh:
nano configure_sssd_ldap.sh
Add the following script (replace placeholders with your LDAP details):
#!/bin/bash

# Install packages
sudo apt update
sudo apt install -y sssd ldap-utils

# Configure SSSD
sudo cat > /etc/sssd/sssd.conf <<EOF
[sssd]
config_file_version = 2
services = nss, pam
domains = default

[domain/default]
id_provider = ldap
auth_provider = ldap
ldap_uri = ldap://ldap.example.com
ldap_search_base = dc=example,dc=com
ldap_user_search_base = ou=users,dc=example,dc=com
ldap_group_search_base = ou=groups,dc=example,dc=com
cache_credentials = True
EOF

# Set permissions and restart SSSD
sudo chmod 600 /etc/sssd/sssd.conf
sudo systemctl restart sssd
Make the script executable:
chmod +x configure_sssd_ldap.sh
Run the script:
sudo ./configure_sssd_ldap.sh
Expected Outcome: SSSD is configured and restarted automatically.
