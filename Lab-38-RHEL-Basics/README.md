SSH Tunneling for Secure Remote Access

Objectives

By the end of this lab, students will be able to:

Understand the concept of SSH tunneling and its use cases
Set up local (-L) and remote (-R) port forwarding using SSH
Test SSH tunnels to securely access remote services
Automate SSH tunneling configurations with a Bash script
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line
Access to a Linux-based cloud machine (provided by Al Nafi - just click "Start Lab")
Two SSH-enabled machines (your local machine and a remote server)
A service running on the remote machine (e.g., a web server on port 8080)
Task 1: Set Up SSH Tunneling

1.1 Local Port Forwarding (ssh -L)

Purpose: Access a remote service as if it were running locally.

Steps:

Open a terminal on your local machine
Run the following command:
ssh -L 9000:localhost:8080 username@remote-server-ip
9000: Local port to forward to
8080: Remote service port
Replace username and remote-server-ip with your credentials
Expected Outcome:

You can now access the remote service on http://localhost:9000 from your local machine
Troubleshooting:

If connection fails, verify:
SSH is allowed on the remote server (sudo systemctl status sshd)
Port 8080 has a running service on the remote machine
1.2 Remote Port Forwarding (ssh -R)

Purpose: Make a local service accessible remotely.

Steps:

On your local machine, run:
ssh -R 9001:localhost:3000 username@remote-server-ip
9001: Remote port to forward to
3000: Local service port
Expected Outcome:

Anyone with access to the remote server can now access your local service at http://remote-server-ip:9001
Task 2: Test SSH Tunneling

2.1 Test Local Forwarding

On your local machine, open a browser
Navigate to http://localhost:9000
Verify you see the remote service (e.g., Apache default page)
2.2 Test Remote Forwarding

SSH into the remote server:
ssh username@remote-server-ip
Run:
curl http://localhost:9001
Verify you see output from your local service
Key Concept: All traffic is encrypted through the SSH tunnel, even for non-SSH protocols like HTTP.

Task 3: Automate SSH Tunneling

3.1 Create a Tunneling Script

Create a file named tunnel.sh:
#!/bin/bash

# Configuration
REMOTE_USER="your_username"
REMOTE_IP="server_ip"
LOCAL_PORT=9000
REMOTE_PORT=8080

# Local forwarding command
echo "Creating local tunnel (Local:$LOCAL_PORT → Remote:$REMOTE_PORT)"
ssh -L $LOCAL_PORT:localhost:$REMOTE_PORT $REMOTE_USER@$REMOTE_IP -Nf
Make it executable:
chmod +x tunnel.sh
3.2 Usage

Start the tunnel:
./tunnel.sh
Check active tunnels:
ps aux | grep ssh
Kill the tunnel:
pkill -f "ssh -L"
Automation Benefit: This script saves time for frequently used tunnels.
