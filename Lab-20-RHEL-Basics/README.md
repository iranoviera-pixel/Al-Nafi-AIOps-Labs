Lab 20: Securing SSH Access with SUDO and SELinux

Objectives

By the end of this lab, students will be able to:

Configure SUDO permissions to control SSH access for specific users
Implement SELinux policies to enhance SSH security
Create automated scripts for SUDO configuration management
Understand the relationship between SUDO and SELinux in SSH access control
Apply security best practices for remote access management
Prerequisites

Before starting this lab, students should have:

Basic understanding of Linux command line operations
Familiarity with SSH concepts and basic usage
Knowledge of user and group management in Linux
Understanding of file permissions and ownership
Basic text editor skills (nano, vim, or similar)
Note: Al Nafi provides ready-to-use Linux-based cloud machines for this lab. Simply click Start Lab to access your pre-configured environment - no need to build your own VM.

Lab Environment Setup

Your Al Nafi cloud machine comes pre-configured with:

CentOS/RHEL-based Linux distribution
SSH service installed and running
SELinux enabled and configured
SUDO package installed
Multiple user accounts for testing
Task 1: Configure SUDO Permissions for SSH Access Control

Subtask 1.1: Understanding Current SSH and SUDO Configuration

First, let's examine the current system configuration to understand our starting point.

Step 1: Check SSH service status

sudo systemctl status sshd
Step 2: Verify SELinux status

sestatus
Step 3: Check current SUDO configuration

sudo cat /etc/sudoers
Step 4: List existing users on the system

cat /etc/passwd | grep -E ":/bin/bash|:/bin/sh" | cut -d: -f1
Subtask 1.2: Create Test Users for SSH Access Control

We'll create several test users to demonstrate different access levels.

Step 1: Create test users

# Create users with different access requirements
sudo useradd -m -s /bin/bash sshuser1
sudo useradd -m -s /bin/bash sshuser2
sudo useradd -m -s /bin/bash restricted_user
sudo useradd -m -s /bin/bash admin_user
Step 2: Set passwords for test users

# Set passwords (use simple passwords for lab purposes)
echo "sshuser1:Password123" | sudo chpasswd
echo "sshuser2:Password123" | sudo chpasswd
echo "restricted_user:Password123" | sudo chpasswd
echo "admin_user:Password123" | sudo chpasswd
Step 3: Create groups for access control

sudo groupadd ssh_allowed
sudo groupadd ssh_admins
Step 4: Add users to appropriate groups

sudo usermod -a -G ssh_allowed sshuser1
sudo usermod -a -G ssh_allowed sshuser2
sudo usermod -a -G ssh_admins admin_user
Subtask 1.3: Configure SSH Access Restrictions

Step 1: Backup the original SSH configuration

sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
Step 2: Edit SSH configuration to restrict access by group

sudo nano /etc/ssh/sshd_config
Add the following lines at the end of the file:

# Allow only specific groups to SSH
AllowGroups ssh_allowed ssh_admins wheel root
DenyUsers restricted_user

# Additional security settings
PermitRootLogin no
PasswordAuthentication yes
PubkeyAuthentication yes
MaxAuthTries 3
ClientAliveInterval 300
ClientAliveCountMax 2
Step 3: Restart SSH service to apply changes

sudo systemctl restart sshd
sudo systemctl status sshd
Subtask 1.4: Configure SUDO Rules for SSH Management

Step 1: Create a custom SUDO configuration file

sudo nano /etc/sudoers.d/ssh_management
Add the following content:

# SSH Management SUDO Rules
# Allow ssh_admins to manage SSH service
%ssh_admins ALL=(ALL) /bin/systemctl restart sshd, /bin/systemctl reload sshd, /bin/systemctl status sshd

# Allow ssh_admins to edit SSH configuration
%ssh_admins ALL=(ALL) /bin/nano /etc/ssh/sshd_config, /bin/vim /etc/ssh/sshd_config

# Allow ssh_admins to view SSH logs
%ssh_admins ALL=(ALL) /bin/journalctl -u sshd, /bin/tail /var/log/secure

# Restrict other users from SSH management
%ssh_allowed ALL=(ALL) !/bin/systemctl * sshd, !/bin/nano /etc/ssh/*, !/bin/vim /etc/ssh/*
Step 2: Validate SUDO configuration syntax

sudo visudo -c -f /etc/sudoers.d/ssh_management
Step 3: Test SUDO permissions

# Switch to admin_user and test SSH management commands
sudo su - admin_user
sudo systemctl status sshd
exit
Task 2: Create Automated SUDO Configuration Script

Subtask 2.1: Design the SUDO Configuration Script

Step 1: Create the script directory

sudo mkdir -p /opt/ssh_security_scripts
cd /opt/ssh_security_scripts
Step 2: Create the main SUDO configuration script

sudo nano configure_ssh_sudo.sh
Add the following content:

#!/bin/bash

# SSH SUDO Configuration Script
# Purpose: Automate SUDO permissions for SSH access control
# Author: Lab 20 - SSH Security Configuration

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log_message() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error_message() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success_message() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning_message() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Function to check if script is run as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error_message "This script must be run as root or with sudo privileges"
        exit 1
    fi
}

# Function to backup existing configurations
backup_configs() {
    log_message "Creating backup of existing configurations..."
    
    # Backup SSH config
    if [[ -f /etc/ssh/sshd_config ]]; then
        cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup.$(date +%Y%m%d_%H%M%S)
        success_message "SSH configuration backed up"
    fi
    
    # Backup existing SUDO rules
    if [[ -f /etc/sudoers.d/ssh_management ]]; then
        cp /etc/sudoers.d/ssh_management /etc/sudoers.d/ssh_management.backup.$(date +%Y%m%d_%H%M%S)
        success_message "SUDO configuration backed up"
    fi
}

# Function to create groups
create_groups() {
    log_message "Creating security groups..."
    
    groups=("ssh_allowed" "ssh_admins" "ssh_restricted")
    
    for group in "${groups[@]}"; do
        if ! getent group "$group" > /dev/null 2>&1; then
            groupadd "$group"
            success_message "Created group: $group"
        else
            warning_message "Group $group already exists"
        fi
    done
}

# Function to configure SUDO rules
configure_sudo_rules() {
    log_message "Configuring SUDO rules for SSH management..."
    
    cat > /etc/sudoers.d/ssh_management << 'EOF'
# SSH Management SUDO Rules - Auto-generated
# Generated on: $(date)

# SSH Administrators - Full SSH management access
%ssh_admins ALL=(ALL) NOPASSWD: /bin/systemctl restart sshd
%ssh_admins ALL=(ALL) NOPASSWD: /bin/systemctl reload sshd
%ssh_admins ALL=(ALL) NOPASSWD: /bin/systemctl status sshd
%ssh_admins ALL=(ALL) NOPASSWD: /bin/systemctl stop sshd
%ssh_admins ALL=(ALL) NOPASSWD: /bin/systemctl start sshd

# SSH Configuration editing
%ssh_admins ALL=(ALL) /bin/nano /etc/ssh/sshd_config
%ssh_admins ALL=(ALL) /bin/vim /etc/ssh/sshd_config
%ssh_admins ALL=(ALL) /bin/vi /etc/ssh/sshd_config

# Log viewing permissions
%ssh_admins ALL=(ALL) NOPASSWD: /bin/journalctl -u sshd*
%ssh_admins ALL=(ALL) NOPASSWD: /bin/tail /var/log/secure
%ssh_admins ALL=(ALL) NOPASSWD: /bin/cat /var/log/secure

# SSH key management
%ssh_admins ALL=(ALL) /bin/ssh-keygen
%ssh_admins ALL=(ALL) /bin/cat /home/*/.ssh/authorized_keys

# Regular SSH users - Limited access
%ssh_allowed ALL=(ALL) NOPASSWD: /bin/systemctl status sshd
%ssh_allowed ALL=(ALL) !/bin/systemctl restart sshd
%ssh_allowed ALL=(ALL) !/bin/systemctl stop sshd
%ssh_allowed ALL=(ALL) !/bin/systemctl start sshd
%ssh_allowed ALL=(ALL) !/bin/nano /etc/ssh/*
%ssh_allowed ALL=(ALL) !/bin/vim /etc/ssh/*
%ssh_allowed ALL=(ALL) !/bin/vi /etc/ssh/*

# Restricted users - No SSH management access
%ssh_restricted ALL=(ALL) !/bin/systemctl * sshd*
%ssh_restricted ALL=(ALL) !/bin/nano /etc/ssh/*
%ssh_restricted ALL=(ALL) !/bin/vim /etc/ssh/*
%ssh_restricted ALL=(ALL) !/bin/vi /etc/ssh/*
EOF

    # Validate SUDO configuration
    if visudo -c -f /etc/sudoers.d/ssh_management; then
        success_message "SUDO rules configured successfully"
    else
        error_message "SUDO configuration validation failed"
        exit 1
    fi
}

# Function to configure SSH restrictions
configure_ssh_restrictions() {
    log_message "Configuring SSH access restrictions..."
    
    # Check if AllowGroups already exists
    if grep -q "^AllowGroups" /etc/ssh/sshd_config; then
        warning_message "AllowGroups already configured in sshd_config"
    else
        echo "" >> /etc/ssh/sshd_config
        echo "# SSH Access Control - Auto-configured" >> /etc/ssh/sshd_config
        echo "AllowGroups ssh_allowed ssh_admins wheel root" >> /etc/ssh/sshd_config
        success_message "SSH group restrictions added"
    fi
    
    # Add additional security settings
    if ! grep -q "MaxAuthTries" /etc/ssh/sshd_config; then
        echo "MaxAuthTries 3" >> /etc/ssh/sshd_config
    fi
    
    if ! grep -q "ClientAliveInterval" /etc/ssh/sshd_config; then
        echo "ClientAliveInterval 300" >> /etc/ssh/sshd_config
        echo "ClientAliveCountMax 2" >> /etc/ssh/sshd_config
    fi
}

# Function to test configuration
test_configuration() {
    log_message "Testing SSH configuration..."
    
    # Test SSH configuration syntax
    if sshd -t; then
        success_message "SSH configuration syntax is valid"
    else
        error_message "SSH configuration syntax error"
        exit 1
    fi
    
    # Restart SSH service
    if systemctl restart sshd; then
        success_message "SSH service restarted successfully"
    else
        error_message "Failed to restart SSH service"
        exit 1
    fi
}

# Function to display summary
display_summary() {
    log_message "Configuration Summary:"
    echo "=================================="
    echo "Groups created:"
    echo "  - ssh_allowed: Regular SSH users"
    echo "  - ssh_admins: SSH administrators"
    echo "  - ssh_restricted: Restricted users"
    echo ""
    echo "SUDO permissions configured:"
    echo "  - ssh_admins: Full SSH management"
    echo "  - ssh_allowed: Limited SSH access"
    echo "  - ssh_restricted: No SSH management"
    echo ""
    echo "SSH restrictions applied:"
    echo "  - Group-based access control"
    echo "  - Enhanced security settings"
    echo "=================================="
}

# Main execution
main() {
    log_message "Starting SSH SUDO configuration script..."
    
    check_root
    backup_configs
    create_groups
    configure_sudo_rules
    configure_ssh_restrictions
    test_configuration
    display_summary
    
    success_message "SSH SUDO configuration completed successfully!"
}

# Execute main function
main "$@"
Step 3: Make the script executable

sudo chmod +x configure_ssh_sudo.sh
Subtask 2.2: Create User Management Helper Script

Step 1: Create a user management script

sudo nano manage_ssh_users.sh
Add the following content:

#!/bin/bash

# SSH User Management Script
# Purpose: Manage users and their SSH access levels

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Functions
log_message() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success_message() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

error_message() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to add user to SSH group
add_user_to_ssh_group() {
    local username=$1
    local group=$2
    
    if [[ -z "$username" || -z "$group" ]]; then
        error_message "Username and group are required"
        return 1
    fi
    
    if ! id "$username" &>/dev/null; then
        error_message "User $username does not exist"
        return 1
    fi
    
    if ! getent group "$group" &>/dev/null; then
        error_message "Group $group does not exist"
        return 1
    fi
    
    usermod -a -G "$group" "$username"
    success_message "Added user $username to group $group"
}

# Function to remove user from SSH group
remove_user_from_ssh_group() {
    local username=$1
    local group=$2
    
    if [[ -z "$username" || -z "$group" ]]; then
        error_message "Username and group are required"
        return 1
    fi
    
    gpasswd -d "$username" "$group" 2>/dev/null || {
        warning_message "User $username was not in group $group"
    }
    success_message "Removed user $username from group $group"
}

# Function to list users in SSH groups
list_ssh_users() {
    log_message "SSH Group Memberships:"
    echo "======================="
    
    for group in ssh_allowed ssh_admins ssh_restricted; do
        if getent group "$group" &>/dev/null; then
            echo -e "${YELLOW}$group:${NC}"
            getent group "$group" | cut -d: -f4 | tr ',' '\n' | sed 's/^/  - /'
            echo ""
        fi
    done
}

# Function to show user's SSH permissions
show_user_permissions() {
    local username=$1
    
    if [[ -z "$username" ]]; then
        error_message "Username is required"
        return 1
    fi
    
    if ! id "$username" &>/dev/null; then
        error_message "User $username does not exist"
        return 1
    fi
    
    log_message "SSH permissions for user: $username"
    echo "=================================="
    
    # Check group memberships
    echo "Group memberships:"
    groups "$username" | cut -d: -f2 | tr ' ' '\n' | grep -E "(ssh_|wheel|root)" | sed 's/^/  - /' || echo "  - No SSH-related groups"
    
    echo ""
    echo "SUDO permissions (SSH-related):"
    sudo -l -U "$username" 2>/dev/null | grep -E "(ssh|systemctl.*sshd)" | sed 's/^/  - /' || echo "  - No SSH-related SUDO permissions"
}

# Main menu
show_menu() {
    echo "SSH User Management Script"
    echo "=========================="
    echo "1. Add user to ssh_allowed group"
    echo "2. Add user to ssh_admins group"
    echo "3. Add user to ssh_restricted group"
    echo "4. Remove user from SSH group"
    echo "5. List all SSH users"
    echo "6. Show user SSH permissions"
    echo "7. Exit"
    echo ""
}

# Main execution
main() {
    if [[ $EUID -ne 0 ]]; then
        error_message "This script must be run as root or with sudo privileges"
        exit 1
    fi
    
    while true; do
        show_menu
        read -p "Select an option (1-7): " choice
        
        case $choice in
            1)
                read -p "Enter username: " username
                add_user_to_ssh_group "$username" "ssh_allowed"
                ;;
            2)
                read -p "Enter username: " username
                add_user_to_ssh_group "$username" "ssh_admins"
                ;;
            3)
                read -p "Enter username: " username
                add_user_to_ssh_group "$username" "ssh_restricted"
                ;;
            4)
                read -p "Enter username: " username
                read -p "Enter group name: " group
                remove_user_from_ssh_group "$username" "$group"
                ;;
            5)
                list_ssh_users
                ;;
            6)
                read -p "Enter username: " username
                show_user_permissions "$username"
                ;;
            7)
                log_message "Exiting..."
                exit 0
                ;;
            *)
                error_message "Invalid option. Please select 1-7."
                ;;
        esac
        
        echo ""
        read -p "Press Enter to continue..."
        clear
    done
}

main "$@"
Step 2: Make the user management script executable

sudo chmod +x manage_ssh_users.sh
Step 3: Test the SUDO configuration script

sudo ./configure_ssh_sudo.sh
Task 3: Implement SELinux Policies for SSH Access Control

Subtask 3.1: Understand Current SELinux SSH Policies

Step 1: Check SELinux status and mode

sestatus
getenforce
Step 2: View current SSH-related SELinux contexts

# Check SSH daemon context
ps -eZ | grep sshd

# Check SSH configuration file contexts
ls -Z /etc/ssh/

# Check SSH port contexts
semanage port -l | grep ssh
Step 3: Check SSH-related SELinux booleans

getsebool -a | grep ssh
Subtask 3.2: Configure SELinux Booleans for SSH Security

Step 1: Review and configure SSH-related SELinux booleans

# Allow SSH to use non-standard ports (if needed)
sudo setsebool -P ssh_sysadm_login on

# Control SSH access for different user types
sudo getsebool ssh_sysadm_login
Step 2: Create a script to manage SELinux SSH settings

sudo nano selinux_ssh_config.sh
Add the following content:

#!/bin/bash

# SELinux SSH Configuration Script
# Purpose: Configure SELinux policies for enhanced SSH security

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_message() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

success_message() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

error_message() {
    echo -e "${RED}[ERROR]${NC} $1"
}

warning_message() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if SELinux is enabled
check_selinux() {
    if ! command -v getenforce &> /dev/null; then
        error_message "SELinux tools not found. Please install policycoreutils."
        exit 1
    fi
    
    local selinux_status=$(getenforce)
    if [[ "$selinux_status" == "Disabled" ]]; then
        error_message "SELinux is disabled. Please enable SELinux and reboot."
        exit 1
    fi
    
    log_message "SELinux status: $selinux_status"
}

# Configure SSH SELinux contexts
configure_ssh_contexts() {
    log_message "Configuring SSH SELinux contexts..."
    
    # Ensure SSH configuration files have correct contexts
    sudo restorecon -R /etc/ssh/
    success_message "SSH configuration contexts restored"
    
    # Set context for custom SSH scripts
    if [[ -d /opt/ssh_security_scripts ]]; then
        sudo semanage fcontext -a -t admin_home_t "/opt/ssh_security_scripts(/.*)?" 2>/dev/null || true
        sudo restorecon -R /opt/ssh_security_scripts/
        success_message "Custom SSH scripts contexts configured"
    fi
}

# Configure SSH SELinux booleans
configure_ssh_booleans() {
    log_message "Configuring SSH SELinux booleans..."
    
    # SSH booleans for enhanced security
    declare -A ssh_booleans=(
        ["ssh_sysadm_login"]="on"
    )
    
    for boolean in "${!ssh_booleans[@]}"; do
        local current_value=$(getsebool "$boolean" | cut -d' ' -f3)
        local desired_value="${ssh_booleans[$boolean]}"
        
        if [[ "$current_value" != "$desired_value" ]]; then
            sudo setsebool -P "$boolean" "$desired_value"
            success_message "Set $boolean to $desired_value"
        else
            log_message "$boolean already set to $desired_value"
        fi
    done
}

# Create custom SELinux policy for SSH management
create_custom_policy() {
    log_message "Creating custom SELinux policy for SSH management..."
    
    # Create policy directory
    sudo mkdir -p /opt/selinux_policies
    cd /opt/selinux_policies
    
    # Create type enforcement file
    cat > ssh_management.te << 'EOF'
module ssh_management 1.0;

require {
    type sshd_t;
    type admin_home_t;
    type etc_t;
    type systemd_unit_file_t;
    class file { read write execute };
    class dir { search };
}

# Allow SSH management scripts to access configuration files
allow admin_home_t etc_t:file { read write };
allow admin_home_t systemd_unit_file_t:file { read };

# Allow SSH daemon to read custom configuration
allow sshd_t admin_home_t:file { read };
allow sshd_t admin_home_t:dir { search };
EOF

    # Compile and install the policy
    if command -v checkmodule &> /dev/null && command -v semodule_package &> /dev/null; then
        checkmodule -M -m -o ssh_management.mod ssh_management.te
        semodule_package -o ssh_management.pp -m ssh_management.mod
        sudo semodule -i ssh_management.pp
        success_message "Custom SELinux policy installed"
    else
        warning_message "SELinux policy development tools not available. Skipping custom policy creation."
    fi
}

# Monitor SSH access with SELinux
setup_selinux_monitoring() {
    log_message "Setting up SELinux monitoring for SSH..."
    
    # Create monitoring script
    cat > /opt/ssh_security_scripts/monitor_ssh_selinux.sh << 'EOF'
#!/bin/bash

# SSH SELinux Monitoring Script

echo "SSH SELinux Status Report"
echo "========================"
echo "Date: $(date)"
echo ""

echo "SELinux Mode: $(getenforce)"
echo ""

echo "SSH-related SELinux Denials (last 24 hours):"
ausearch -m avc -ts recent | grep ssh || echo "No SSH-related denials found"
echo ""

echo "SSH SELinux Booleans:"
getsebool -a | grep ssh
echo ""

echo "SSH Process Contexts:"
ps -eZ | grep sshd
echo ""

echo "SSH File Contexts:"
ls -Z /etc/ssh/sshd_config
echo ""
EOF

    chmod +x /opt/ssh_security_scripts/monitor_ssh_selinux.sh
    success_message "SELinux monitoring script created"
}

# Function to test SELinux configuration
test_selinux_config() {
    log_message "Testing SELinux SSH configuration..."
    
    # Test SSH service start with current SELinux policy
    if sudo systemctl restart sshd; then
        success_message "SSH service started successfully with SELinux policies"
    else
        error_message "SSH service failed to start. Check SELinux denials."
        return 1
    fi
    
    # Check for recent SELinux denials
    local denials=$(ausearch -m avc -ts recent 2>/dev/null | grep ssh | wc -l)
    if [[ $denials -eq 0 ]]; then
        success_message "No recent SELinux denials for SSH"
    else
        warning_message "Found $denials recent SELinux denials for SSH. Check logs."
    fi
}

# Display configuration summary
display_summary() {
    log_message "SELinux SSH Configuration Summary:"
    echo "=================================="
    echo "SELinux Mode: $(getenforce)"
    echo ""
    echo "SSH SELinux Booleans:"
    getsebool -a | grep ssh | sed 's/^/  /'
    echo ""
    echo "SSH Service Status:"
    systemctl is-active sshd
    echo ""
    echo "Monitoring script: /opt/ssh_security_scripts/monitor_ssh_selinux.sh"
    echo "=================================="
}

# Main execution
main() {
    if [[ $EUID -ne 0 ]]; then
        error_message "This script must be run as root or with sudo privileges"
        exit 1
    fi
    
    log_message "Starting SELinux SSH configuration..."
    
    check_selinux
    configure_ssh_contexts
    configure_ssh_booleans
    create_custom_policy
    setup_selinux_monitoring
    test_selinux_config
    display_summary
    
    success_message "SELinux SSH configuration completed successfully!"
}

main "$@"
Step 3: Make the SELinux script executable and run it

sudo chmod +x selinux_ssh_config.sh
sudo ./selinux_ssh_config.sh
Subtask 3.3: Create Automated SELinux Policy Update Script

Step 1: Create an automated policy update script

sudo nano update_selinux_ssh_policies.sh
Add the following content:

#!/bin/bash

# Automated SELinux SSH Policy Update Script
# Purpose: Automatically update and maintain SELinux policies for SSH

set -e

# Configuration
POLICY_DIR="/opt/selinux_policies"
LOG_FILE="/var/log/selinux_ssh_updates.log"
BACKUP_DIR="/opt/selinux_policies/backups"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging function
log_to_file() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log_message() {
    local message="$1"
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $message"
    log_to_file "$message"
}

success_message() {
    local message="$1"
    echo -e "${GREEN}[SUCCESS]${NC} $message"
    log_to_file "SUCCESS: $message"
}

error_message() {
    local message="$1"
    echo -e "${RED}[ERROR]${NC} $message"
    log_to_file "ERROR: $message"
}

warning_message() {
    local message="$1"
    echo -e "${YELLOW}[WARNING]${NC} $message"
    log_to_file "WARNING: $message"
}

# Initialize directories
initialize_directories() {
    sudo mkdir -p "$POLICY_DIR" "$BACKUP_DIR"
    sudo touch "$LOG_FILE"
    log_message "Initialized policy directories"
}

# Backup current policies
backup_current_policies() {
    log_message "Backing up current SELinux policies..."
    
    local backup_timestamp=$(date +%Y%m%d_%H%M%S)
    local backup_path="$BACKUP_DIR/backup_$backup_timestamp"
    
    sudo mkdir -p "$backup_path"
    
    # Backup current SSH-related policies
    sudo semodule -l | grep ssh > "$backup_path/ssh_modules.list" 2>/dev/null || true
    
    # Export current booleans
    sudo getsebool -a | grep ssh > "$backup_path/ssh_booleans.list" 2>/dev/null || true
    
    success_message "Policies backed up to $backup_path"
}

# Check for SELinux denials
check_selinux_denials() {
    log_message "Checking for recent SELinux denials..."
    
    local denial_count=0
    local temp_file="/tmp/ssh_denials_$$.log"
    
    # Check for SSH-related denials in the last hour
    ausearch -m avc -ts recent 2>/dev/null | grep ssh > "$temp_file" || true
    
    if [[ -s "$temp_file" ]]; then
        denial_count=$(wc -l < "$temp_file")
        warning_message "Found $denial_count SSH-related SELinux denials"
        
        # Log the denials
        log_message "Recent SSH SELinux denials:"
        cat "$temp_file" >> "$LOG_FILE"
        
        # Generate policy suggestions
        generate_policy_suggestions "$temp_file"
    else
        success_message "No recent SSH-related SELinux denials found"
    fi
    
    rm -f "$temp_file"
    return $denial_count
}

# Generate policy suggestions based on denials
generate_policy_suggestions() {
    local denial_file="$1"
    log_
