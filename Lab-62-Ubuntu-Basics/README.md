Lab 62: Securing the SSH Protocol

Objectives

By the end of this lab, you will be able to:

Understand SSH security best practices
Configure key-based authentication for SSH
Harden SSH server configuration
Automate SSH security configurations using scripts
Disable password-based authentication for improved security
Prerequisites

A Linux system (Ubuntu/CentOS recommended)
Sudo or root access
Basic Linux command line knowledge
SSH server installed (openssh-server)
Setup Requirements

Ensure SSH server is installed:
sudo apt-get install openssh-server  # Ubuntu/Debian
sudo yum install openssh-server      # CentOS/RHEL
Verify SSH service is running:
sudo systemctl status ssh
Task 1: Configure Key-Based Authentication and Disable Password Login

Subtask 1.1: Generate SSH Key Pair

On your client machine, generate a new SSH key pair:

ssh-keygen -t ed25519 -a 100
Press Enter to accept default file path
Enter a strong passphrase (recommended)
View your public key:

cat ~/.ssh/id_ed25519.pub
Subtask 1.2: Copy Public Key to Server

Copy the public key to your server:

ssh-copy-id username@server_ip
Enter your password when prompted
Alternatively, manually add the key:

ssh username@server_ip "mkdir -p ~/.ssh && chmod 700 ~/.ssh"
cat ~/.ssh/id_ed25519.pub | ssh username@server_ip "cat >> ~/.ssh/authorized_keys && chmod 600 ~/.ssh/authorized_keys"
Subtask 1.3: Test Key-Based Authentication

Attempt to SSH using your key:
ssh username@server_ip
You should be logged in without a password (or with your key passphrase)
Subtask 1.4: Disable Password Authentication

Edit the SSH server configuration:

sudo nano /etc/ssh/sshd_config
Find and modify these lines:

PasswordAuthentication no
ChallengeResponseAuthentication no
UsePAM no
Restart SSH service:

sudo systemctl restart ssh
Expected Outcome: You can only log in using SSH keys, password authentication is disabled.

Troubleshooting Tip: If locked out, access the server console directly and temporarily re-enable password authentication.

Task 2: SSH Hardening via /etc/ssh/sshd_config

Subtask 2.1: Basic Hardening

Edit the configuration file:

sudo nano /etc/ssh/sshd_config
Apply these security settings:

PermitRootLogin no
MaxAuthTries 3
LoginGraceTime 1m
ClientAliveInterval 300
ClientAliveCountMax 2
Subtask 2.2: Protocol and Encryption Settings

Add/modify these lines:
Protocol 2
HostKey /etc/ssh/ssh_host_ed25519_key
HostKey /etc/ssh/ssh_host_rsa_key
KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com,umask 077
Subtask 2.3: Apply Changes

Check configuration syntax:

sudo sshd -t
Restart SSH service:

sudo systemctl restart ssh
Expected Outcome: SSH service runs with enhanced security settings, using modern cryptographic algorithms.

Troubleshooting Tip: If SSH fails to start, check system logs with journalctl -u ssh for errors.

Task 3: Automation Script for SSH Configuration

Subtask 3.1: Create Configuration Script

Create a new script file:

nano secure_ssh.sh
Add the following content:

#!/bin/bash

# Backup original config
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.bak

# Apply security settings
sudo sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/^#Protocol 2/Protocol 2/' /etc/ssh/sshd_config

# Add modern cryptographic settings
echo -e "KexAlgorithms curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256\nCiphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com,aes128-gcm@openssh.com,aes256-ctr,aes192-ctr,aes128-ctr\nMACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com" | sudo tee -a /etc/ssh/sshd_config > /dev/null

# Restart SSH service
sudo systemctl restart ssh

echo "SSH hardening complete!"
Subtask 3.2: Make Script Executable

Set permissions:

chmod +x secure_ssh.sh
Run the script:

sudo ./secure_ssh.sh
Expected Outcome: All SSH security configurations are applied automatically with a single script execution.

Troubleshooting Tip: Always test the script in a non-production environment first.

