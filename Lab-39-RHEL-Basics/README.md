Automating SSH Key Management

Objectives

By the end of this lab, students will be able to:

Generate SSH key pairs using ssh-keygen
Distribute public keys to remote systems using ssh-copy-id
Automate SSH key management for new users with a Bash script
Understand the security benefits of key-based authentication
Prerequisites

Before starting this lab, you should have:

Basic familiarity with Linux command line
Access to a Linux system (Al Nafi provides cloud machines - just click "Start Lab")
Two or more Linux systems that can communicate over SSH (we'll use localhost for practice)
openssh-client and openssh-server packages installed (pre-installed on most Linux distros)
Lab Setup

Click "Start Lab" to launch your cloud machine
Open a terminal window
Verify SSH is installed by running:
ssh -V
Expected output: OpenSSH_<version>
Task 1: Generate SSH Keys Using ssh-keygen

Step 1.1: Generate a New SSH Key Pair

Run the following command to generate a 4096-bit RSA key pair:
ssh-keygen -t rsa -b 4096
When prompted:
Press Enter to accept the default file location (~/.ssh/id_rsa)
Enter a passphrase (optional but recommended for security)
Confirm the passphrase
Expected Output:

Generating public/private rsa key pair.
Enter file in which to save the key (/home/user/.ssh/id_rsa):
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/user/.ssh/id_rsa
Your public key has been saved in /home/user/.ssh/id_rsa.pub
Step 1.2: Verify Key Generation

List the contents of your .ssh directory:
ls -l ~/.ssh/
You should see two new files:
id_rsa (private key - NEVER share this)
id_rsa.pub (public key - safe to share)
Troubleshooting Tip: If you get "Permission denied" when trying to access .ssh, run chmod 700 ~/.ssh

Task 2: Distribute SSH Public Keys Using ssh-copy-id

Step 2.1: Prepare Target Systems

For this lab, we'll use localhost as our target, but in real scenarios you would use remote server IPs.

First, ensure SSH server is running:
sudo systemctl start sshd
Step 2.2: Copy Public Key to Target

Use ssh-copy-id to install your public key:
ssh-copy-id localhost
Enter your password when prompted
Expected Output:

Number of key(s) added: 1
Now try logging into the machine with: "ssh 'localhost'"
Step 2.3: Test Passwordless Login

Verify you can now SSH without a password:
ssh localhost
You should be logged in without being prompted for a password (only passphrase if you set one)
Troubleshooting Tip: If prompted for password:

Ensure ~/.ssh/authorized_keys on the target has correct permissions (600)
Verify the public key was properly appended to authorized_keys
Task 3: Automate SSH Key Management for New Users

Step 3.1: Create the Automation Script

Create a new file called add_ssh_user.sh:
nano add_ssh_user.sh
Add the following script:
#!/bin/bash

# Check for required arguments
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <username> <remote_server>"
    exit 1
fi

USERNAME=$1
SERVER=$2

# Generate SSH key pair if it doesn't exist
if [ ! -f "/home/$USERNAME/.ssh/id_rsa" ]; then
    echo "Generating new SSH key pair for $USERNAME..."
    sudo -u $USERNAME ssh-keygen -t rsa -b 4096 -f "/home/$USERNAME/.ssh/id_rsa" -N ""
fi

# Copy public key to remote server
echo "Copying public key to $SERVER..."
sudo -u $USERNAME ssh-copy-id $USERNAME@$SERVER

echo "SSH key setup complete for $USERNAME on $SERVER"
Step 3.2: Make the Script Executable

Set execute permissions:
chmod +x add_ssh_user.sh
Step 3.3: Test the Script

First create a test user:
sudo adduser testuser
Run the script:
sudo ./add_ssh_user.sh testuser localhost
Verify it worked by switching to the test user and testing SSH:
sudo su - testuser
ssh localhost
exit
Troubleshooting Tip: If you get permission errors:

Ensure the script is run with sudo
Check that the user's home directory exists
Verify the remote server allows SSH key authentication (check /etc/ssh/sshd_config for PubkeyAuthentication yes)
