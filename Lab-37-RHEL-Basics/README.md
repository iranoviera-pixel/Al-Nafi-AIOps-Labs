SSH Hardening

Objectives

By the end of this lab, you will be able to:

Understand the importance of SSH security.
Disable root login via SSH to prevent brute-force attacks.
Configure key-based authentication for secure SSH access.
Write a script to automate SSH hardening.
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge (e.g., cd, ls, nano).
Access to a Linux-based cloud machine (provided by Al Nafi—click Start Lab to launch).
A non-root user with sudo privileges (created automatically in the Al Nafi lab environment).
Task 1: Disable Root Login in /etc/ssh/sshd_config

Why?

Allowing root login via SSH is a security practice. Attackers often target the root account. Disabling it forces users to log in as a regular user and escalate privileges using sudo.

Steps:

Open the SSH configuration file:

sudo nano /etc/ssh/sshd_config
Find the line (use Ctrl+W to search):

#PermitRootLogin yes
Uncomment and modify it to:

PermitRootLogin no
Save and exit (Ctrl+O, Enter, Ctrl+X).

Restart the SSH service:

sudo systemctl restart sshd
Expected Outcome:

Root login via SSH is now disabled. Verify by attempting (in a new terminal):
ssh root@localhost
You should see: Permission denied (publickey).
Troubleshooting:

If SSH fails to restart, check for syntax errors:
sudo sshd -t
Task 2: Configure SSH Key-Based Authentication

Why?

Passwords can be cracked. Key-based authentication uses cryptographic keys, which are more secure.

Steps:

Generate an SSH key pair (on your local machine or Al Nafi lab):

ssh-keygen -t ed25519 -a 100
Press Enter to accept the default file location (~/.ssh/id_ed25519).
Optional: Add a passphrase for extra security.
Copy the public key to the server:

ssh-copy-id username@your_server_ip
Replace username with your Al Nafi lab username and your_server_ip with localhost (if working locally).

Verify key-based login:

ssh username@localhost
You should log in without a password (or with your key’s passphrase).
Expected Outcome:

Password-less login works. Check the server’s ~/.ssh/authorized_keys file to confirm your public key was added.
Task 3: Write a Script to Harden SSH

Why?

Automating SSH hardening ensures consistency across systems and saves time.

Steps:

Create a script file:

nano harden_ssh.sh
Add the following code:

#!/bin/bash
# Backup the original SSH config
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Disable root login and password authentication
sudo sed -i 's/^#PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config

# Restart SSH
sudo systemctl restart sshd
echo "SSH hardening complete. Password login disabled."
Make the script executable:

chmod +x harden_ssh.sh
Run the script:

sudo ./harden_ssh.sh
Expected Outcome:

Password authentication is disabled. Verify by attempting:
ssh username@localhost
Without a key, you’ll see: Permission denied (publickey).
Troubleshooting:

If locked out, restore the backup:
sudo cp /etc/ssh/sshd_config.bak /etc/ssh/sshd_config
sudo systemctl restart sshd
