Lab 53: Configuring Samba File Services

Objectives

By the end of this lab, you will be able to:

Install and configure a Samba server on a Linux system.
Create and manage shared directories using Samba.
Automate Samba service management with a Bash script.
Verify Samba file sharing functionality.
Prerequisites

A Linux system (Ubuntu 20.04/22.04 or CentOS 7/8)
sudo or root access
Basic Linux command-line knowledge
Network connectivity
Task 1: Install and Configure Samba Server

Subtask 1.1: Install Samba Packages

Command for Ubuntu/Debian:

sudo apt update
sudo apt install samba -y
Command for CentOS/RHEL:

sudo yum install samba samba-client -y
Expected Outcome:

Samba packages are installed without errors.
Verify with: sudo smbd --version
Subtask 1.2: Configure Samba

Backup the original configuration file:

sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
Edit the configuration:

sudo nano /etc/samba/smb.conf
Add these global settings under the [global] section:

workgroup = WORKGROUP
server string = Samba Server %v
netbios name = ubuntu
security = user
map to guest = bad user
dns proxy = no
Key Concept:

workgroup should match your Windows workgroup (default: WORKGROUP).
security = user enforces Samba to use local user authentication.
Task 2: Share Directories via Samba

Subtask 2.1: Create a Shared Directory

Create a directory and set permissions:

sudo mkdir -p /samba/share
sudo chown nobody:nogroup /samba/share
sudo chmod 777 /samba/share
Add the share configuration to /etc/samba/smb.conf:

[public]
path = /samba/share
browsable = yes
writable = yes
guest ok = yes
read only = no
Subtask 2.2: Restart Samba Services

sudo systemctl restart smbd nmbd
sudo systemctl enable smbd nmbd
Troubleshooting Tip:
If services fail to start, check logs with:
journalctl -xe or tail -f /var/log/samba/log.smbd

Task 3: Automate Samba Management with a Script

Subtask 3.1: Create a Bash Script

Create /usr/local/bin/samba_manager.sh with the following content:

#!/bin/bash

# Check if Samba is running
status_samba() {
    systemctl is-active smbd >/dev/null 2>&1 && echo "Samba is RUNNING" || echo "Samba is STOPPED"
}

# Start Samba services
start_samba() {
    sudo systemctl start smbd nmbd
    status_samba
}

# Stop Samba services
stop_samba() {
    sudo systemctl stop smbd nmbd
    status_samba
}

# Main menu
case "$1" in
    start)
        start_samba
        ;;
    stop)
        stop_samba
        ;;
    status)
        status_samba
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        exit 1
esac
Subtask 3.2: Make the Script Executable

sudo chmod +x /usr/local/bin/samba_manager.sh
Testing the Script:

Start Samba: sudo samba_manager.sh start
Check status: sudo samba_manager.sh status

