Lab 62: SSH Key Management

Objectives

By the end of this lab, you will be able to:

Understand the concept of SSH key-based authentication
Generate SSH key pairs using ssh-keygen
Distribute public keys to remote systems using ssh-copy-id
Automate SSH key distribution across multiple machines with a script
Improve security by replacing password-based authentication with SSH keys
Prerequisites

Before starting this lab, you should have:

Basic familiarity with Linux command line
Access to a Linux-based cloud machine (provided by Al Nafi - just click "Start Lab")
Two or more Linux machines (or one local and one remote) for testing key distribution
SSH client already installed (default on most Linux distributions)
Lab Setup

Al Nafi provides pre-configured Linux cloud machines for this lab:

Simply click "Start Lab" to launch your environment
You'll receive two machines: client-machine and server-machine
Both machines are pre-configured with SSH access
Task 1: Generate SSH Keys Using ssh-keygen

Step 1.1: Check for Existing SSH Keys

Before generating new keys, check if you already have SSH keys:

ls -al ~/.ssh
Expected Output:

If no keys exist, you'll see "No such file or directory"
If keys exist, you'll see files like id_rsa (private key) and id_rsa.pub (public key)
Step 1.2: Generate a New SSH Key Pair

Generate a new RSA key pair (2048-bit):

ssh-keygen -t rsa -b 2048
Follow the prompts:

Press Enter to accept default file location (~/.ssh/id_rsa)
Enter a passphrase (optional but recommended for security)
Confirm the passphrase
Expected Output:

Generating public/private rsa key pair.
Your identification has been saved in /home/user/.ssh/id_rsa
Your public key has been saved in /home/user/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:AbCdEfGhIjKlMnOpQrStUvWxYz1234567890 user@client-machine
Step 1.3: Verify Key Generation

Check that the keys were created:

ls -l ~/.ssh/id_rsa*
Expected Output:

-rw------- 1 user user 1766 Mar 1 10:00 /home/user/.ssh/id_rsa
-rw-r--r-- 1 user user  394 Mar 1 10:00 /home/user/.ssh/id_rsa.pub
Key Concepts:

Private key (id_rsa): Keep this secure - never share it
Public key (id_rsa.pub): Can be safely shared with remote systems
Task 2: Distribute SSH Keys Using ssh-copy-id

Step 2.1: Prepare the Remote Server

Ensure SSH is running on the target server:

# On server-machine:
sudo systemctl status ssh
Troubleshooting: If SSH isn't running: sudo systemctl start ssh

Step 2.2: Copy Public Key to Remote Server

From your client machine:

ssh-copy-id user@server-machine
Follow the prompts:

Enter "yes" to confirm the server's fingerprint (first time only)
Enter the remote user's password
Expected Output:

Number of key(s) added: 1
Now try logging into the machine with: "ssh user@server-machine"
Step 2.3: Test Passwordless Login

Verify the key authentication works:

ssh user@server-machine
Expected Behavior:

If you set a passphrase, you'll be prompted for it
If no passphrase, you'll login directly
You should NOT be asked for the remote user's password
Task 3: Automate SSH Key Distribution

Step 3.1: Create a List of Target Servers

Create a file with server IPs/hostnames:

echo "server-machine" > servers.txt
# Add more servers if available:
# echo "server2" >> servers.txt
# echo "server3" >> servers.txt
Step 3.2: Create the Distribution Script

Create distribute_keys.sh:

#!/bin/bash

# Read each server from the list
while read server; do
    echo "Distributing key to $server..."
    
    # Check if key exists, generate if not
    if [ ! -f ~/.ssh/id_rsa.pub ]; then
        ssh-keygen -t rsa -b 2048 -N "" -f ~/.ssh/id_rsa
    fi
    
    # Copy the key
    ssh-copy-id -i ~/.ssh/id_rsa.pub user@$server
    
    # Test the connection
    ssh -o PasswordAuthentication=no user@$server "echo 'Key authentication successful on $server'"
    
done < servers.txt
Step 3.3: Make the Script Executable and Run It

chmod +x distribute_keys.sh
./distribute_keys.sh
Security Note: The -N "" flag creates a key without a passphrase (less secure). In production, either:

Omit this flag and enter passphrase manually, or
Use SSH agent for passphrase management
