Lab 73: Installing and Configuring Squid Proxy Server

Objectives

By the end of this lab, you will be able to:

Install and configure the Squid proxy server on a Linux system.
Set up basic Squid configurations, including cache directory and access control lists (ACLs).
Write and execute a script to manage proxy access.
Prerequisites

A Linux system (Ubuntu 20.04/22.04 or CentOS 7/8)
Sudo or root privileges
Basic knowledge of Linux command line and text editors (e.g., nano, vim)
Task 1: Install Squid Proxy Server on Linux

Subtask 1.1: Update System Packages

Before installing Squid, ensure your system packages are up to date.

Commands:

sudo apt update && sudo apt upgrade -y      # For Ubuntu/Debian
sudo yum update -y                          # For CentOS/RHEL
Expected Outcome:
All system updates are applied successfully.

Subtask 1.2: Install Squid

Install the Squid package using the package manager.

Commands:

sudo apt install squid -y                   # For Ubuntu/Debian
sudo yum install squid -y                   # For CentOS/RHEL
Expected Outcome:
Squid is installed and the service is enabled.

Subtask 1.3: Verify Installation

Check the Squid service status to confirm it is running.

Commands:

sudo systemctl status squid
Expected Outcome:
Output shows active (running) status.

Troubleshooting Tip:
If Squid fails to start, check logs using:

sudo journalctl -u squid
Task 2: Configure Basic Squid Settings

Subtask 2.1: Configure Cache Directory

Squid stores cached data in a directory. Configure the cache size and location.

Steps:

Open the Squid configuration file:

sudo nano /etc/squid/squid.conf
Locate the cache_dir directive and modify it (or add if missing):

cache_dir ufs /var/spool/squid 100 16 256
ufs: Storage format
/var/spool/squid: Cache directory
100: Maximum cache size in MB
16: First-level subdirectories
256: Second-level subdirectories
Save and exit (Ctrl+O, Enter, Ctrl+X).

Expected Outcome:
Squid will use the specified directory for caching.

Subtask 2.2: Configure Access Control Lists (ACLs)

Restrict access to the proxy server using ACLs.

Steps:

Open /etc/squid/squid.conf again.
Add the following ACL rules to allow only specific IPs (e.g., 192.168.1.0/24):
acl local_net src 192.168.1.0/24
http_access allow local_net
http_access deny all
Save and exit.
Expected Outcome:
Only clients from 192.168.1.0/24 can use the proxy.

Subtask 2.3: Restart Squid

Apply changes by restarting Squid.

Command:

sudo systemctl restart squid
Verification:
Test proxy access from an allowed IP using curl:

curl -x http://<PROXY_IP>:3128 http://example.com
Task 3: Script for Proxy Access Management

Subtask 3.1: Write a Bash Script

Create a script to automate Squid ACL updates.

Script (manage_squid.sh):

#!/bin/bash

# Check for root
if [ "$(id -u)" -ne 0 ]; then
  echo "Run as root!" >&2
  exit 1
fi

# Add or remove ACL entries
case "$1" in
  add)
    echo "acl $2 src $3" >> /etc/squid/squid.conf
    echo "http_access allow $2" >> /etc/squid/squid.conf
    systemctl restart squid
    echo "Added $2 ($3) to ACL."
    ;;
  remove)
    sed -i "/acl $2 src/d" /etc/squid/squid.conf
    sed -i "/http_access allow $2/d" /etc/squid/squid.conf
    systemctl restart squid
    echo "Removed $2 from ACL."
    ;;
  *)
    echo "Usage: $0 {add|remove} <acl_name> <ip_range>"
    exit 1
    ;;
esac
Subtask 3.2: Make the Script Executable

chmod +x manage_squid.sh
Subtask 3.3: Test the Script

Add an ACL:
sudo ./manage_squid.sh add office_network 10.0.0.0/24
Remove an ACL:
sudo ./manage_squid.sh remove office_network
Expected Outcome:
The script updates /etc/squid/squid.conf and restarts Squid.

