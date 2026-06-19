Lab 48: Integrating SELinux with System Services

Objectives

By the end of this lab, students will be able to:

• Understand the fundamentals of SELinux and its role in system security • Enable and configure SELinux for specific services including Apache, MySQL, and SSH • Modify SELinux policies to implement service-specific access control • Create and execute scripts to automate SELinux configuration and verification • Troubleshoot common SELinux issues with system services • Implement best practices for SELinux integration in production environments

Prerequisites

Before starting this lab, students should have:

• Basic understanding of Linux command line operations • Familiarity with system services and service management • Knowledge of file permissions and ownership concepts • Understanding of web servers, databases, and SSH concepts • Access to a terminal or command prompt

Note: Al Nafi provides ready-to-use Linux-based cloud machines for this lab. Simply click Start Lab to begin - no need to build your own virtual machine.

Lab Environment Setup

Initial System Preparation

Before we begin working with SELinux, let's prepare our system and understand the current state.

Step 1: Check Current SELinux Status

First, let's examine the current SELinux configuration on our system.

# Check SELinux status
sestatus

# Check current enforcement mode
getenforce

# View SELinux configuration file
cat /etc/selinux/config
Step 2: Install Required Packages

Install the necessary packages for this lab:

# Update system packages
sudo yum update -y

# Install SELinux utilities
sudo yum install -y policycoreutils-python-utils setools-console

# Install services we'll be working with
sudo yum install -y httpd mariadb-server openssh-server

# Install additional SELinux tools
sudo yum install -y setroubleshoot-server selinux-policy-devel
Task 1: Enable and Configure SELinux for Apache Web Server

Subtask 1.1: Enable SELinux in Enforcing Mode

Let's start by ensuring SELinux is properly enabled and configured.

# Set SELinux to enforcing mode temporarily
sudo setenforce 1

# Verify the change
getenforce

# Make the change permanent by editing the config file
sudo sed -i 's/SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config

# Verify the configuration
grep SELINUX= /etc/selinux/config
Subtask 1.2: Configure Apache with SELinux

Now let's set up Apache web server with proper SELinux integration.

# Start and enable Apache service
sudo systemctl start httpd
sudo systemctl enable httpd

# Check Apache service status
sudo systemctl status httpd

# Verify Apache is running and check SELinux context
ps -eZ | grep httpd
Subtask 1.3: Configure SELinux Contexts for Web Content

Set up proper SELinux contexts for web content directories.

# Create a custom web directory
sudo mkdir -p /var/www/custom

# Create a sample HTML file
sudo tee /var/www/custom/index.html > /dev/null << 'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>SELinux Apache Test</title>
</head>
<body>
    <h1>Apache with SELinux Integration</h1>
    <p>This page is served by Apache with SELinux protection.</p>
</body>
</html>
EOF

# Check current SELinux context
ls -Z /var/www/custom/

# Set proper SELinux context for web content
sudo semanage fcontext -a -t httpd_exec_t "/var/www/custom(/.*)?"
sudo restorecon -R /var/www/custom/

# Verify the context change
ls -Z /var/www/custom/
Subtask 1.4: Configure Apache Virtual Host with SELinux

Create a virtual host configuration that works with SELinux.

# Create virtual host configuration
sudo tee /etc/httpd/conf.d/custom.conf > /dev/null << 'EOF'
<VirtualHost *:80>
    ServerName localhost
    DocumentRoot /var/www/custom
    <Directory /var/www/custom>
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
EOF

# Test Apache configuration
sudo httpd -t

# Restart Apache to apply changes
sudo systemctl restart httpd

# Test the web server
curl http://localhost/
Task 2: Configure SELinux for MySQL/MariaDB

Subtask 2.1: Install and Configure MariaDB

Set up MariaDB database server with SELinux integration.

# Start and enable MariaDB
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Check MariaDB process context
ps -eZ | grep mysql

# Secure MariaDB installation
sudo mysql_secure_installation
Subtask 2.2: Configure SELinux for Database Operations

Configure SELinux to allow database operations and network connections.

# Allow MariaDB to use network connections
sudo setsebool -P mysql_connect_any 1

# Allow database to write to user home directories (if needed)
sudo setsebool -P mysql_connect_http 1

# Check current boolean settings
getsebool -a | grep mysql

# Create a custom database directory
sudo mkdir -p /opt/mysql_data
sudo chown mysql:mysql /opt/mysql_data

# Set SELinux context for custom database directory
sudo semanage fcontext -a -t mysqld_db_t "/opt/mysql_data(/.*)?"
sudo restorecon -R /opt/mysql_data/

# Verify context
ls -Z /opt/mysql_data/
Subtask 2.3: Test Database Connectivity

Test database operations under SELinux protection.

# Connect to MariaDB and create test database
sudo mysql -u root -p << 'EOF'
CREATE DATABASE selinux_test;
USE selinux_test;
CREATE TABLE test_table (id INT PRIMARY KEY, name VARCHAR(50));
INSERT INTO test_table VALUES (1, 'SELinux Test');
SELECT * FROM test_table;
EXIT;
EOF

# Check for any SELinux denials
sudo ausearch -m avc -ts recent
Task 3: Configure SELinux for SSH Service

Subtask 3.1: Configure SSH with Custom Port

Configure SSH to run on a custom port with proper SELinux integration.

# Backup original SSH configuration
sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Configure SSH to use port 2222
sudo sed -i 's/#Port 22/Port 2222/' /etc/ssh/sshd_config

# Add the new port to SELinux policy
sudo semanage port -a -t ssh_port_t -p tcp 2222

# Verify the port addition
sudo semanage port -l | grep ssh

# Restart SSH service
sudo systemctl restart sshd

# Check SSH service status
sudo systemctl status sshd
Subtask 3.2: Configure SELinux Booleans for SSH

Configure SELinux booleans to control SSH behavior.

# View SSH-related booleans
getsebool -a | grep ssh

# Allow SSH to use port forwarding (if needed)
sudo setsebool -P ssh_sysadm_login 1

# Allow SSH to connect to all ports (if needed for tunneling)
sudo setsebool -P ssh_keysign 1

# Verify boolean settings
getsebool ssh_sysadm_login ssh_keysign
Task 4: Create Comprehensive SELinux Configuration Script

Subtask 4.1: Create the Main Configuration Script

Create a comprehensive script to configure and verify SELinux settings for all services.

# Create the main configuration script
sudo tee /usr/local/bin/selinux_service_config.sh > /dev/null << 'EOF'
#!/bin/bash

# SELinux Service Configuration Script
# This script configures SELinux for Apache, MariaDB, and SSH services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

warning() {
    echo -e "${YELLOW}[WARNING] $1${NC}"
}

# Function to check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error "This script must be run as root"
        exit 1
    fi
}

# Function to check SELinux status
check_selinux() {
    log "Checking SELinux status..."
    
    if ! command -v sestatus &> /dev/null; then
        error "SELinux tools not installed"
        exit 1
    fi
    
    local status=$(getenforce)
    log "Current SELinux status: $status"
    
    if [[ "$status" != "Enforcing" ]]; then
        warning "SELinux is not in enforcing mode"
        log "Setting SELinux to enforcing mode..."
        setenforce 1
        sed -i 's/SELINUX=.*/SELINUX=enforcing/' /etc/selinux/config
    fi
}

# Function to configure Apache with SELinux
configure_apache() {
    log "Configuring Apache with SELinux..."
    
    # Ensure Apache is installed and running
    if ! systemctl is-active --quiet httpd; then
        log "Starting Apache service..."
        systemctl start httpd
        systemctl enable httpd
    fi
    
    # Set up custom web directory
    mkdir -p /var/www/selinux_test
    
    # Create test page
    cat > /var/www/selinux_test/index.html << 'HTML'
<!DOCTYPE html>
<html>
<head>
    <title>SELinux Apache Configuration Test</title>
</head>
<body>
    <h1>Apache with SELinux - Configuration Successful!</h1>
    <p>This page demonstrates successful SELinux integration with Apache.</p>
    <p>Timestamp: $(date)</p>
</body>
</html>
HTML
    
    # Set proper SELinux contexts
    semanage fcontext -a -t httpd_exec_t "/var/www/selinux_test(/.*)?" 2>/dev/null || true
    restorecon -R /var/www/selinux_test/
    
    # Create virtual host
    cat > /etc/httpd/conf.d/selinux_test.conf << 'VHOST'
<VirtualHost *:80>
    ServerName selinux-test.local
    DocumentRoot /var/www/selinux_test
    <Directory /var/www/selinux_test>
        AllowOverride None
        Require all granted
    </Directory>
</VirtualHost>
VHOST
    
    # Test and restart Apache
    httpd -t && systemctl restart httpd
    
    log "Apache configuration completed"
}

# Function to configure MariaDB with SELinux
configure_mariadb() {
    log "Configuring MariaDB with SELinux..."
    
    # Ensure MariaDB is running
    if ! systemctl is-active --quiet mariadb; then
        log "Starting MariaDB service..."
        systemctl start mariadb
        systemctl enable mariadb
    fi
    
    # Set SELinux booleans for MariaDB
    setsebool -P mysql_connect_any 1
    setsebool -P mysql_connect_http 1
    
    # Create custom data directory
    mkdir -p /opt/mysql_custom
    chown mysql:mysql /opt/mysql_custom
    
    # Set SELinux context
    semanage fcontext -a -t mysqld_db_t "/opt/mysql_custom(/.*)?" 2>/dev/null || true
    restorecon -R /opt/mysql_custom/
    
    log "MariaDB configuration completed"
}

# Function to configure SSH with SELinux
configure_ssh() {
    log "Configuring SSH with SELinux..."
    
    # Add custom SSH port to SELinux policy
    local custom_port=2222
    semanage port -a -t ssh_port_t -p tcp $custom_port 2>/dev/null || true
    
    # Set SSH booleans
    setsebool -P ssh_sysadm_login 1
    
    log "SSH configuration completed"
}

# Function to verify configurations
verify_configurations() {
    log "Verifying SELinux configurations..."
    
    echo "=== SELinux Status ==="
    sestatus
    echo
    
    echo "=== Apache Process Context ==="
    ps -eZ | grep httpd | head -3
    echo
    
    echo "=== MariaDB Process Context ==="
    ps -eZ | grep mysql | head -3
    echo
    
    echo "=== SSH Process Context ==="
    ps -eZ | grep sshd | head -3
    echo
    
    echo "=== SELinux Booleans ==="
    echo "MySQL booleans:"
    getsebool -a | grep mysql
    echo "SSH booleans:"
    getsebool -a | grep ssh | head -5
    echo
    
    echo "=== SELinux Ports ==="
    semanage port -l | grep -E "(http_port_t|ssh_port_t)" | head -5
    echo
    
    echo "=== File Contexts ==="
    echo "Web directories:"
    ls -Z /var/www/ | head -5
    echo "MySQL directories:"
    ls -Z /var/lib/mysql/ | head -3 2>/dev/null || echo "MySQL data directory not accessible"
    echo
}

# Function to check for SELinux denials
check_denials() {
    log "Checking for recent SELinux denials..."
    
    local denials=$(ausearch -m avc -ts recent 2>/dev/null | wc -l)
    if [[ $denials -gt 0 ]]; then
        warning "Found $denials recent SELinux denials"
        echo "Recent denials:"
        ausearch -m avc -ts recent 2>/dev/null | tail -10
    else
        log "No recent SELinux denials found"
    fi
}

# Main execution
main() {
    log "Starting SELinux service configuration..."
    
    check_root
    check_selinux
    configure_apache
    configure_mariadb
    configure_ssh
    verify_configurations
    check_denials
    
    log "SELinux service configuration completed successfully!"
    log "You can now test your services with SELinux protection enabled."
}

# Run main function
main "$@"
EOF

# Make the script executable
sudo chmod +x /usr/local/bin/selinux_service_config.sh
Subtask 4.2: Create Service Verification Script

Create a script to verify that all services are working correctly with SELinux.

# Create verification script
sudo tee /usr/local/bin/verify_selinux_services.sh > /dev/null << 'EOF'
#!/bin/bash

# SELinux Service Verification Script

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

error() {
    echo -e "${RED}[ERROR] $1${NC}"
}

success() {
    echo -e "${GREEN}[SUCCESS] $1${NC}"
}

# Test Apache
test_apache() {
    log "Testing Apache service..."
    
    if systemctl is-active --quiet httpd; then
        success "Apache service is running"
        
        # Test web access
        if curl -s http://localhost/ > /dev/null; then
            success "Apache is responding to HTTP requests"
        else
            error "Apache is not responding to HTTP requests"
        fi
        
        # Check SELinux context
        local context=$(ps -eZ | grep httpd | head -1 | awk '{print $1}')
        log "Apache SELinux context: $context"
        
    else
        error "Apache service is not running"
    fi
}

# Test MariaDB
test_mariadb() {
    log "Testing MariaDB service..."
    
    if systemctl is-active --quiet mariadb; then
        success "MariaDB service is running"
        
        # Test database connection
        if mysql -u root -e "SELECT 1;" &>/dev/null; then
            success "MariaDB is accepting connections"
        else
            error "MariaDB connection failed"
        fi
        
        # Check SELinux context
        local context=$(ps -eZ | grep mysql | head -1 | awk '{print $1}')
        log "MariaDB SELinux context: $context"
        
    else
        error "MariaDB service is not running"
    fi
}

# Test SSH
test_ssh() {
    log "Testing SSH service..."
    
    if systemctl is-active --quiet sshd; then
        success "SSH service is running"
        
        # Check if custom port is configured
        local custom_port=$(grep "^Port" /etc/ssh/sshd_config | awk '{print $2}')
        if [[ -n "$custom_port" && "$custom_port" != "22" ]]; then
            log "SSH is configured on custom port: $custom_port"
        fi
        
        # Check SELinux context
        local context=$(ps -eZ | grep sshd | head -1 | awk '{print $1}')
        log "SSH SELinux context: $context"
        
    else
        error "SSH service is not running"
    fi
}

# Check SELinux status
check_selinux_status() {
    log "Checking overall SELinux status..."
    
    local status=$(getenforce)
    if [[ "$status" == "Enforcing" ]]; then
        success "SELinux is in enforcing mode"
    else
        error "SELinux is not in enforcing mode: $status"
    fi
    
    # Check for recent denials
    local denials=$(ausearch -m avc -ts today 2>/dev/null | wc -l)
    if [[ $denials -eq 0 ]]; then
        success "No SELinux denials found today"
    else
        error "Found $denials SELinux denials today"
    fi
}

# Main execution
main() {
    log "Starting SELinux service verification..."
    echo
    
    check_selinux_status
    echo
    
    test_apache
    echo
    
    test_mariadb
    echo
    
    test_ssh
    echo
    
    log "Verification completed!"
}

main "$@"
EOF

# Make the verification script executable
sudo chmod +x /usr/local/bin/verify_selinux_services.sh
Subtask 4.3: Execute the Configuration Scripts

Now let's run our scripts to configure and verify everything.

# Run the main configuration script
sudo /usr/local/bin/selinux_service_config.sh

# Wait a moment for services to stabilize
sleep 5

# Run the verification script
sudo /usr/local/bin/verify_selinux_services.sh
Task 5: Advanced SELinux Policy Modifications

Subtask 5.1: Create Custom SELinux Policy Module

Create a custom SELinux policy module for specific application needs.

# Create a directory for custom policies
sudo mkdir -p /etc/selinux/custom_policies
cd /etc/selinux/custom_policies

# Create a custom policy file
sudo tee custom_web_app.te > /dev/null << 'EOF'
module custom_web_app 1.0;

require {
    type httpd_t;
    type httpd_exec_t;
    type var_t;
    class file { read write create unlink };
    class dir { search write add_name remove_name };
}

# Allow httpd to write to /var/log/custom_app
allow httpd_t var_t:dir { search write add_name remove_name };
allow httpd_t var_t:file { read write create unlink };
EOF

# Compile the policy module
sudo checkmodule -M -m -o custom_web_app.mod custom_web_app.te

# Create policy package
sudo semodule_package -o custom_web_app.pp -m custom_web_app.mod

# Install the custom policy
sudo semodule -i custom_web_app.pp

# Verify installation
sudo semodule -l | grep custom_web_app
Subtask 5.2: Monitor and Troubleshoot SELinux

Set up monitoring and troubleshooting tools.

# Install and configure setroubleshoot
sudo yum install -y setroubleshoot-server

# Start the troubleshooting service
sudo systemctl start setroubleshoot
sudo systemctl enable setroubleshoot

# Create a monitoring script
sudo tee /usr/local/bin/selinux_monitor.sh > /dev/null << 'EOF'
#!/bin/bash

# SELinux Monitoring Script

echo "=== SELinux Status ==="
sestatus
echo

echo "=== Recent SELinux Alerts ==="
if command -v sealert &> /dev/null; then
    sealert -l "*" 2>/dev/null | tail -20
else
    echo "sealert not available"
fi
echo

echo "=== Recent AVC Denials ==="
ausearch -m avc -ts recent 2>/dev/null | tail -10 || echo "No recent denials"
echo

echo "=== SELinux Booleans Status ==="
echo "Critical booleans:"
getsebool httpd_can_network_connect
getsebool mysql_connect_any
getsebool ssh_sysadm_login
echo

echo "=== Service Contexts ==="
echo "Apache processes:"
ps -eZ | grep httpd | head -3
echo "MySQL processes:"
ps -eZ | grep mysql | head -3
echo "SSH processes:"
ps -eZ | grep sshd | head -3
EOF

sudo chmod +x /usr/local/bin/selinux_monitor.sh

# Run the monitoring script
sudo /usr/local/bin/selinux_monitor.sh
