Lab 80: Setting Up Load Balancer Network

Objectives

By the end of this lab, you will be able to:

Understand the basics of load balancing and its importance in distributed systems
Set up and configure HAProxy or Nginx as a load balancer
Configure backend servers to distribute traffic evenly
Automate load balancer configuration using a Bash script
Prerequisites

Basic understanding of Linux command line
Three Ubuntu 20.04/22.04 servers (1 for load balancer, 2 for backend servers)
sudo or root access on all servers
SSH access between servers
Basic knowledge of networking concepts (IP addresses, ports)
Task 1: Setting Up HAProxy for Load Balancing

Subtask 1.1: Install HAProxy on Load Balancer Server

SSH into your load balancer server
Update package lists and install HAProxy:
sudo apt update
sudo apt install haproxy -y
Verify installation:
haproxy -v
Expected Output: HAProxy version information

Subtask 1.2: Configure HAProxy

Backup the original configuration file:
sudo cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.bak
Edit the configuration file:
sudo nano /etc/haproxy/haproxy.cfg
Add this configuration (replace IPs with your backend servers):
global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5000
    timeout client 50000
    timeout server 50000

frontend http_front
    bind *:80
    stats uri /haproxy?stats
    default_backend http_back

backend http_back
    balance roundrobin
    server backend1 192.168.1.101:80 check
    server backend2 192.168.1.102:80 check
Save and exit (Ctrl+X, Y, Enter)
Subtask 1.3: Start and Enable HAProxy

sudo systemctl restart haproxy
sudo systemctl enable haproxy
Verification:

sudo systemctl status haproxy
Expected Outcome: Active (running) status

Task 2: Configure Backend Servers

Subtask 2.1: Set Up Web Servers on Backend Nodes

On each backend server (192.168.1.101 and 192.168.1.102 in this example):

Install Nginx:
sudo apt update
sudo apt install nginx -y
Create unique content for each server:
echo "<h1>Server 1</h1>" | sudo tee /var/www/html/index.html  # On server 1
echo "<h1>Server 2</h1>" | sudo tee /var/www/html/index.html  # On server 2
Start and enable Nginx:
sudo systemctl start nginx
sudo systemctl enable nginx
Subtask 2.2: Test Backend Servers

curl http://localhost
Expected Output: The respective server's HTML content

Task 3: Automate Load Balancer Configuration

Subtask 3.1: Create Automation Script

On your load balancer server:

Create a new script file:
nano lb_automation.sh
Add this script (adjust IPs as needed):
#!/bin/bash

# Define backend servers
BACKEND1="192.168.1.101"
BACKEND2="192.168.1.102"

# Install HAProxy if not installed
if ! command -v haproxy &> /dev/null
then
    echo "Installing HAProxy..."
    sudo apt update
    sudo apt install haproxy -y
fi

# Configure HAProxy
echo "Configuring HAProxy..."
sudo bash -c "cat > /etc/haproxy/haproxy.cfg" <<EOF
global
    log /dev/log local0
    log /dev/log local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s
    user haproxy
    group haproxy
    daemon

defaults
    log global
    mode http
    option httplog
    option dontlognull
    timeout connect 5000
    timeout client 50000
    timeout server 50000

frontend http_front
    bind *:80
    stats uri /haproxy?stats
    default_backend http_back

backend http_back
    balance roundrobin
    server backend1 $BACKEND1:80 check
    server backend2 $BACKEND2:80 check
EOF

# Restart HAProxy
echo "Restarting HAProxy..."
sudo systemctl restart haproxy

echo "Load balancer configuration complete!"
Make the file executable:
chmod +x lb_automation.sh
Run the script:
sudo ./lb_automation.sh
Expected Outcome: Successful installation and configuration of HAProxy

Testing and Verification

From your local machine or another server, test the load balancer:
curl http://<load-balancer-ip>
Refresh multiple times - you should see responses alternating between Server 1 and Server 2

Check HAProxy statistics:

In a web browser, visit: http://<load-balancer-ip>/haproxy?stats

