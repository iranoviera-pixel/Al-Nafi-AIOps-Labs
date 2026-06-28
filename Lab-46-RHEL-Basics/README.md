Lab 46: Automating SELinux Security Management

Objectives

By the end of this lab, students will be able to:

Understand SELinux modes and policies.
Automate SELinux policy configuration for multiple services.
Switch between SELinux modes (Enforcing, Permissive, Disabled) using scripts.
Check SELinux status and restart services programmatically.
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge.
A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Administrative (root) access or sudo privileges.
Familiarity with text editors like nano or vim.
Lab Setup

Access Your Lab Machine:
Click Start Lab on the Al Nafi platform to launch your Linux cloud machine.
Verify SELinux Installation:
Run the following command to check if SELinux is installed:
sestatus
Expected Output: Displays current SELinux status (e.g., "SELinux status: enabled").
Task 1: Configure SELinux Policies for Multiple Services

Subtasks

Create a Script to Add Policies:

Open a new file named selinux_policy_manager.sh:
nano selinux_policy_manager.sh
Paste the following script:
#!/bin/bash
# This script configures SELinux policies for HTTPD, FTP, and SSH services.

# Define services
SERVICES=("httpd" "ftpd" "sshd")

for service in "${SERVICES[@]}"; do
    echo "Configuring SELinux policy for $service..."
    sudo setsebool -P $(echo $service)_enable_homedirs on
    sudo setsebool -P $(echo $service)_anon_write on
    echo "$service policy updated."
done
Save and exit (Ctrl+O, Enter, Ctrl+X).
Make the Script Executable:

chmod +x selinux_policy_manager.sh
Run the Script:

sudo ./selinux_policy_manager.sh
Expected Output: Success messages for each service policy update.
Troubleshooting

If a service isn’t installed (e.g., ftpd), install it first:
sudo yum install vsftpd -y  # For CentOS/RHEL
sudo apt-get install vsftpd -y  # For Ubuntu
Task 2: Automate SELinux Mode Switching

Subtasks

Create a Mode-Switching Script:

Open selinux_mode_switcher.sh:
nano selinux_mode_switcher.sh
Paste the script:
#!/bin/bash
# This script switches SELinux modes based on user input.

echo "Select SELinux mode:"
echo "1. Enforcing"
echo "2. Permissive"
echo "3. Disabled"
read -p "Enter choice (1-3): " choice

case $choice in
    1) sudo setenforce 1 && echo "SELinux set to Enforcing." ;;
    2) sudo setenforce 0 && echo "SELinux set to Permissive." ;;
    3) sudo sed -i 's/SELINUX=.*/SELINUX=disabled/' /etc/selinux/config \
       && echo "SELinux will be disabled after reboot." ;;
    *) echo "Invalid choice. Exiting." ;;
esac
Run the Script:

chmod +x selinux_mode_switcher.sh
sudo ./selinux_mode_switcher.sh
Expected Output: Mode change confirmation or error for invalid input.
Key Concept

Enforcing: Blocks unauthorized actions.
Permissive: Logs but allows violations.
Disabled: Turns off SELinux (requires reboot).
Task 3: Check SELinux Status and Restart Services

Subtasks

Create a Status-Check Script:

Open selinux_service_checker.sh:
nano selinux_service_checker.sh
Paste the script:
#!/bin/bash
# This script checks SELinux status and restarts affected services.

STATUS=$(getenforce)
echo "Current SELinux status: $STATUS"

if [ "$STATUS" == "Enforcing" ]; then
    echo "Restarting services for policy changes to take effect..."
    sudo systemctl restart httpd sshd vsftpd
    echo "Services restarted."
else
    echo "No restart needed (SELinux not in Enforcing mode)."
fi
Execute the Script:

chmod +x selinux_service_checker.sh
sudo ./selinux_service_checker.sh
Expected Output: Current status and service restart confirmation (if applicable).
