Lab 16: Integrating LDAP Authentication for SSH Access

Objectives

By the end of this lab, students will be able to:

Understand LDAP authentication for SSH.
Configure sssd (System Security Services Daemon) to integrate LDAP authentication.
Modify SSH configuration to allow LDAP users to log in securely.
Write and apply a script to enforce security settings for LDAP-based SSH access.
Prerequisites

Before starting this lab, ensure you have:

A Linux-based machine (Ubuntu 20.04/22.04 or CentOS 7/8). (Note: Al Nafi provides pre-configured cloud machines—click Start Lab to begin.)
Basic familiarity with Linux command line.
Admin (sudo) privileges on the machine.
An LDAP server with user accounts (e.g., OpenLDAP). (For testing, you can use a free LDAP server like FreeIPA or a demo LDAP server.)
Task 1: Install and Configure SSSD for LDAP Authentication

Step 1: Install Required Packages

Run the following commands to install sssd and LDAP tools:

sudo apt update && sudo apt install -y sssd ldap-utils libnss-ldap libpam-ldap
(For CentOS/RHEL: sudo yum install -y sssd openldap-clients)

Expected Output: Packages install without errors.

Step 2: Configure SSSD

Edit the SSSD configuration file:
sudo nano /etc/sssd/sssd.conf
Add the following configuration (replace ldap.example.com and dc=example,dc=com with your LDAP server details):
[sssd]
config_file_version = 2
services = nss, pam
domains = example.com

[domain/example.com]
id_provider = ldap
auth_provider = ldap
ldap_uri = ldap://ldap.example.com
ldap_search_base = dc=example,dc=com
ldap_user_search_base = ou=users,dc=example,dc=com
ldap_group_search_base = ou=groups,dc=example,dc=com
ldap_default_bind_dn = cn=admin,dc=example,dc=com
ldap_default_authtok = admin_password
cache_credentials = True
Set correct permissions:
sudo chmod 600 /etc/sssd/sssd.conf
sudo systemctl restart sssd
Verification:

ldapsearch -x -H ldap://ldap.example.com -b "dc=example,dc=com"
(Should list LDAP users.)

Task 2: Modify SSH Configuration for LDAP

Step 1: Update PAM and NSS

Edit /etc/nsswitch.conf:

sudo nano /etc/nsswitch.conf
Modify these lines:

passwd:         compat sss
group:          compat sss
shadow:         compat sss
Restart services:

sudo pam-auth-update  # Enable LDAP authentication)
sudo systemctl restart ssh
Step 2: Test LDAP User Login

Attempt SSH login as an LDAP user:
ssh ldapuser@localhost
(Replace ldapuser with an existing LDAP username.)
Expected Outcome: Successful login if credentials are correct.

Task 3: Script to Enforce Security Settings

Step 1: Create a Security Script

Write a script (ldap_ssh_security.sh):
#!/bin/bash
# Ensure LDAP users have secure SSH access
echo "Enforcing SSH security for LDAP users..."

# Disable root login
sudo sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config

# Allow only LDAP users (replace with your LDAP group)
echo "AllowGroups sshusers" | sudo tee -a /etc/ssh/sshd_config

# Restart SSH
sudo systemctl restart sshd
echo "LDAP SSH security applied!"
Make it executable and run:
chmod +x ldap_ssh_security.sh
sudo ./ldap_ssh_security.sh
Verification:

sudo sshd -T | grep PermitRootLogin  # Should return "no"
Troubleshooting Tips

SSSD Not Starting: Check logs with journalctl -u sssd.
LDAP Connection Issues: Verify LDAP URI and bind credentials in /etc/sssd/sssd.conf.
SSH Access Denied: Ensure the LDAP user is in the sshusers group (or adjust AllowGroups).
