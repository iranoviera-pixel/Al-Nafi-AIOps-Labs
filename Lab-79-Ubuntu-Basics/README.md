Lab 79: Introduction to Load Balancing

Objectives

By the end of this lab, you will:

Understand fundamental load balancing techniques (round-robin, least connections).
Configure basic load balancing using ipvs or haproxy.
Write a script to distribute traffic across multiple backend servers.
Gain hands-on experience with open-source load balancing tools.
Prerequisites

A Linux system (Ubuntu 22.04/Debian 11/CentOS 8) with root/sudo access.
Basic familiarity with Linux commands and networking.
Two or more backend servers (can be virtual machines or containers) running a simple web service (e.g., Apache/Nginx).
Task 1: Research Load Balancing Techniques

Subtask 1.1: Understand Key Concepts

Round-Robin: Distributes requests sequentially across servers.
Least Connections: Routes traffic to the server with the fewest active connections.
IP Hash: Uses client IP to assign a fixed server for session persistence.
Subtask 1.2: Compare Tools

IPVS: Kernel-based load balancer (high performance, L4).
HAProxy: Application-layer load balancer (L7, more features).
Task 2: Set Up Basic Load Balancing

Option A: Using IPVS (L4 Load Balancing)

Subtask 2.1: Install IPVS

sudo apt update && sudo apt install ipvsadm -y  # Debian/Ubuntu
sudo dnf install ipvsadm -y                     # CentOS/RHEL
Subtask 2.2: Configure IPVS Load Balancer

Enable IP forwarding:
echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
Add backend servers (replace SERVER_IP_1/2 with actual IPs):
sudo ipvsadm -A -t <LOAD_BALANCER_IP>:80 -s rr
sudo ipvsadm -a -t <LOAD_BALANCER_IP>:80 -r SERVER_IP_1:80 -m
sudo ipvsadm -a -t <LOAD_BALANCER_IP>:80 -r SERVER_IP_2:80 -m
-s rr: Round-robin scheduling.
-m: Masquerading (NAT).
Subtask 2.3: Verify Configuration

sudo ipvsadm -Ln
Expected Output:

TCP  <LOAD_BALANCER_IP>:80 rr
  -> SERVER_IP_1:80            Masq    1      0      0
  -> SERVER_IP_2:80            Masq    1      0      0
Option B: Using HAProxy (L7 Load Balancing)

Subtask 2.4: Install HAProxy

sudo apt install haproxy -y  # Debian/Ubuntu
sudo dnf install haproxy -y  # CentOS/RHEL
Subtask 2.5: Configure HAProxy

Edit /etc/haproxy/haproxy.cfg:

frontend http_front
   bind *:80
   default_backend http_back

backend http_back
   balance roundrobin
   server server1 SERVER_IP_1:80 check
   server server2 SERVER_IP_2:80 check
Subtask 2.6: Start HAProxy

sudo systemctl enable --now haproxy
sudo systemctl status haproxy  # Verify running
Task 3: Traffic Distribution Script

Subtask 3.1: Python Script to Simulate Traffic

import requests
import time

servers = ["http://SERVER_IP_1", "http://SERVER_IP_2"]

for i in range(10):
    for server in servers:
        try:
            response = requests.get(server)
            print(f"Request to {server}: Status {response.status_code}")
        except Exception as e:
            print(f"Error connecting to {server}: {e}")
    time.sleep(1)
Expected Outcome:
Requests alternate between servers (round-robin) or follow the configured algorithm.

