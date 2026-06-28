Lab 54: Tuning sysctl for Performance

Objectives

By the end of this lab, students will be able to:

• Understand what sysctl is and how it manages kernel parameters • View current kernel parameter values using sysctl commands • Modify kernel parameters temporarily and permanently • Tune file descriptor limits for better application performance • Optimize network parameters for improved connectivity • Adjust memory management settings for system efficiency • Create automated scripts to apply sysctl configurations • Configure sysctl settings to persist across system reboots • Troubleshoot common sysctl configuration issues

Prerequisites

Before starting this lab, students should have:

• Basic understanding of Linux command line interface • Familiarity with text editors like nano or vim • Knowledge of basic system administration concepts • Understanding of file permissions and ownership • Basic scripting knowledge (helpful but not required)

Ready-to-Use Cloud Machines

Al Nafi provides pre-configured Linux-based cloud machines for this lab. Simply click Start Lab to access your virtual environment. No need to build your own VM or install additional software - everything is ready to use!

Lab Environment Setup

Your cloud machine comes with: • Ubuntu 20.04 LTS or CentOS 8 • Root access for system configuration • All necessary tools pre-installed • Network connectivity for testing

Task 1: Understanding and Using sysctl to View Kernel Parameters

Subtask 1.1: Introduction to sysctl

sysctl is a powerful tool that allows you to view and modify kernel parameters at runtime. Think of it as the control panel for your Linux system's core behavior.

First, let's explore what sysctl can show us:

# View all available kernel parameters (this will show hundreds of parameters)
sysctl -a | head -20

# View a specific parameter
sysctl kernel.hostname

# View parameters in a specific category
sysctl kernel.* | head -10
Subtask 1.2: Exploring Key Parameter Categories

Let's examine the main categories of kernel parameters:

# System information parameters
sysctl kernel.ostype
sysctl kernel.osrelease
sysctl kernel.version

# Process and file limits
sysctl fs.file-max
sysctl fs.file-nr

# Network parameters
sysctl net.core.somaxconn
sysctl net.ipv4.tcp_max_syn_backlog

# Memory management
sysctl vm.swappiness
sysctl vm.dirty_ratio
Subtask 1.3: Understanding Parameter Format

Kernel parameters follow a hierarchical structure:

# Format: category.subcategory.parameter
# Examples:
echo "Network core parameters:"
sysctl net.core.rmem_max
sysctl net.core.wmem_max

echo "Virtual memory parameters:"
sysctl vm.overcommit_memory
sysctl vm.panic_on_oom
Task 2: Tuning Parameters for File Descriptors, Networking, and Memory

Subtask 2.1: File Descriptor Tuning

File descriptors are handles that processes use to access files, sockets, and other I/O resources. Let's optimize these limits:

# Check current file descriptor limits
echo "Current file descriptor limits:"
sysctl fs.file-max
sysctl fs.file-nr
ulimit -n

# View current usage
echo "Current file descriptor usage:"
cat /proc/sys/fs/file-nr
Now let's tune these parameters:

# Temporarily increase file descriptor limits
sudo sysctl fs.file-max=2097152
sudo sysctl fs.nr_open=1048576

# Verify the changes
sysctl fs.file-max
sysctl fs.nr_open

# Set per-process limits (requires editing limits.conf)
echo "Setting per-process limits..."
Create a script to check file descriptor usage:

# Create a monitoring script
cat > check_fd_usage.sh << 'EOF'
#!/bin/bash
echo "=== File Descriptor Usage Report ==="
echo "System-wide limit: $(cat /proc/sys/fs/file-max)"
echo "Currently allocated: $(cat /proc/sys/fs/file-nr | cut -f1)"
echo "Currently used: $(cat /proc/sys/fs/file-nr | cut -f2)"
echo "Maximum ever used: $(cat /proc/sys/fs/file-nr | cut -f3)"
echo ""
echo "Per-process limit: $(ulimit -n)"
echo ""
echo "Top processes by open files:"
lsof | awk '{print $2}' | sort | uniq -c | sort -nr | head -5
EOF

chmod +x check_fd_usage.sh
./check_fd_usage.sh
Subtask 2.2: Network Parameter Tuning

Network tuning can significantly improve performance for high-traffic applications:

# Check current network parameters
echo "Current network settings:"
sysctl net.core.somaxconn
sysctl net.core.netdev_max_backlog
sysctl net.ipv4.tcp_max_syn_backlog
sysctl net.ipv4.tcp_fin_timeout
sysctl net.ipv4.tcp_keepalive_time
Apply network optimizations:

# Increase connection queue sizes
sudo sysctl net.core.somaxconn=65535
sudo sysctl net.core.netdev_max_backlog=5000
sudo sysctl net.ipv4.tcp_max_syn_backlog=8192

# Optimize TCP settings
sudo sysctl net.ipv4.tcp_fin_timeout=30
sudo sysctl net.ipv4.tcp_keepalive_time=1200
sudo sysctl net.ipv4.tcp_keepalive_probes=3
sudo sysctl net.ipv4.tcp_keepalive_intvl=15

# Increase buffer sizes
sudo sysctl net.core.rmem_max=134217728
sudo sysctl net.core.wmem_max=134217728
sudo sysctl net.ipv4.tcp_rmem="4096 87380 134217728"
sudo sysctl net.ipv4.tcp_wmem="4096 65536 134217728"

# Enable TCP window scaling
sudo sysctl net.ipv4.tcp_window_scaling=1
Create a network performance test script:

cat > network_test.sh << 'EOF'
#!/bin/bash
echo "=== Network Performance Parameters ==="
echo "Connection queue limit: $(sysctl -n net.core.somaxconn)"
echo "Network device backlog: $(sysctl -n net.core.netdev_max_backlog)"
echo "TCP SYN backlog: $(sysctl -n net.ipv4.tcp_max_syn_backlog)"
echo "TCP FIN timeout: $(sysctl -n net.ipv4.tcp_fin_timeout)"
echo ""
echo "Buffer sizes:"
echo "Max receive buffer: $(sysctl -n net.core.rmem_max)"
echo "Max send buffer: $(sysctl -n net.core.wmem_max)"
echo ""
echo "Current connections:"
ss -s
EOF

chmod +x network_test.sh
./network_test.sh
Subtask 2.3: Memory Management Tuning

Memory parameters control how the kernel manages RAM and swap:

# Check current memory settings
echo "Current memory management settings:"
sysctl vm.swappiness
sysctl vm.dirty_ratio
sysctl vm.dirty_background_ratio
sysctl vm.overcommit_memory
sysctl vm.overcommit_ratio
Apply memory optimizations:

# Reduce swappiness (prefer RAM over swap)
sudo sysctl vm.swappiness=10

# Adjust dirty page ratios for better I/O performance
sudo sysctl vm.dirty_ratio=15
sudo sysctl vm.dirty_background_ratio=5

# Configure memory overcommit
sudo sysctl vm.overcommit_memory=1
sudo sysctl vm.overcommit_ratio=50

# Optimize cache pressure
sudo sysctl vm.vfs_cache_pressure=50

# Set minimum free memory
sudo sysctl vm.min_free_kbytes=65536
Create a memory monitoring script:

cat > memory_monitor.sh << 'EOF'
#!/bin/bash
echo "=== Memory Management Report ==="
echo "Swappiness: $(sysctl -n vm.swappiness)"
echo "Dirty ratio: $(sysctl -n vm.dirty_ratio)%"
echo "Dirty background ratio: $(sysctl -n vm.dirty_background_ratio)%"
echo "Overcommit memory: $(sysctl -n vm.overcommit_memory)"
echo ""
echo "Current memory usage:"
free -h
echo ""
echo "Swap usage:"
swapon --show
echo ""
echo "Cache pressure: $(sysctl -n vm.vfs_cache_pressure)"
echo "Min free memory: $(sysctl -n vm.min_free_kbytes) KB"
EOF

chmod +x memory_monitor.sh
./memory_monitor.sh
Task 3: Creating Automation Scripts and Persistent Configuration

Subtask 3.1: Creating a Comprehensive Tuning Script

Let's create a script that applies all our optimizations:

cat > system_tuning.sh << 'EOF'
#!/bin/bash

# System Performance Tuning Script
# This script applies optimized sysctl settings for better performance

echo "=== Starting System Performance Tuning ==="
echo "Timestamp: $(date)"
echo ""

# Backup current settings
echo "Creating backup of current settings..."
sysctl -a > /tmp/sysctl_backup_$(date +%Y%m%d_%H%M%S).txt
echo "Backup saved to /tmp/sysctl_backup_$(date +%Y%m%d_%H%M%S).txt"
echo ""

# File Descriptor Tuning
echo "Applying file descriptor optimizations..."
sysctl -w fs.file-max=2097152
sysctl -w fs.nr_open=1048576
echo "✓ File descriptor limits increased"

# Network Tuning
echo "Applying network optimizations..."
sysctl -w net.core.somaxconn=65535
sysctl -w net.core.netdev_max_backlog=5000
sysctl -w net.ipv4.tcp_max_syn_backlog=8192
sysctl -w net.ipv4.tcp_fin_timeout=30
sysctl -w net.ipv4.tcp_keepalive_time=1200
sysctl -w net.core.rmem_max=134217728
sysctl -w net.core.wmem_max=134217728
sysctl -w net.ipv4.tcp_window_scaling=1
echo "✓ Network parameters optimized"

# Memory Management Tuning
echo "Applying memory management optimizations..."
sysctl -w vm.swappiness=10
sysctl -w vm.dirty_ratio=15
sysctl -w vm.dirty_background_ratio=5
sysctl -w vm.overcommit_memory=1
sysctl -w vm.overcommit_ratio=50
sysctl -w vm.vfs_cache_pressure=50
sysctl -w vm.min_free_kbytes=65536
echo "✓ Memory management optimized"

echo ""
echo "=== Tuning Complete ==="
echo "All optimizations have been applied successfully!"
echo "Note: These changes are temporary and will be lost on reboot."
echo "Use the persistent configuration script to make them permanent."
EOF

chmod +x system_tuning.sh
Subtask 3.2: Creating Persistent Configuration

To make changes permanent, we need to modify the sysctl configuration file:

# Create a backup of the original sysctl.conf
sudo cp /etc/sysctl.conf /etc/sysctl.conf.backup

# Create our optimized configuration
cat > optimized_sysctl.conf << 'EOF'
# Optimized sysctl configuration for performance
# Generated by Lab 54: Tuning sysctl for Performance

# File Descriptor Limits
fs.file-max = 2097152
fs.nr_open = 1048576

# Network Performance
net.core.somaxconn = 65535
net.core.netdev_max_backlog = 5000
net.ipv4.tcp_max_syn_backlog = 8192
net.ipv4.tcp_fin_timeout = 30
net.ipv4.tcp_keepalive_time = 1200
net.ipv4.tcp_keepalive_probes = 3
net.ipv4.tcp_keepalive_intvl = 15
net.core.rmem_max = 134217728
net.core.wmem_max = 134217728
net.ipv4.tcp_window_scaling = 1

# Memory Management
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
vm.overcommit_memory = 1
vm.overcommit_ratio = 50
vm.vfs_cache_pressure = 50
vm.min_free_kbytes = 65536

# Security Settings
kernel.dmesg_restrict = 1
kernel.kptr_restrict = 1
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
EOF
Subtask 3.3: Creating Installation and Management Scripts

Create a script to install the persistent configuration:

cat > install_sysctl_config.sh << 'EOF'
#!/bin/bash

# Script to install persistent sysctl configuration

if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root or with sudo"
    exit 1
fi

echo "=== Installing Persistent sysctl Configuration ==="
echo ""

# Create backup
echo "Creating backup of current configuration..."
cp /etc/sysctl.conf /etc/sysctl.conf.backup.$(date +%Y%m%d_%H%M%S)
echo "✓ Backup created"

# Install new configuration
echo "Installing optimized configuration..."
cp optimized_sysctl.conf /etc/sysctl.d/99-performance.conf
echo "✓ Configuration installed to /etc/sysctl.d/99-performance.conf"

# Apply settings immediately
echo "Applying settings..."
sysctl -p /etc/sysctl.d/99-performance.conf
echo "✓ Settings applied"

# Verify installation
echo ""
echo "Verifying installation..."
if [ -f /etc/sysctl.d/99-performance.conf ]; then
    echo "✓ Configuration file exists"
    echo "✓ Settings will persist across reboots"
else
    echo "✗ Installation failed"
    exit 1
fi

echo ""
echo "=== Installation Complete ==="
echo "Your system is now optimized for performance!"
echo "Settings will automatically apply on system startup."
EOF

chmod +x install_sysctl_config.sh
Create a verification script:

cat > verify_sysctl.sh << 'EOF'
#!/bin/bash

# Script to verify sysctl configuration

echo "=== sysctl Configuration Verification ==="
echo "Timestamp: $(date)"
echo ""

# Check if our configuration file exists
if [ -f /etc/sysctl.d/99-performance.conf ]; then
    echo "✓ Performance configuration file found"
else
    echo "✗ Performance configuration file not found"
    echo "Run install_sysctl_config.sh first"
    exit 1
fi

echo ""
echo "Current parameter values:"
echo "========================"

# File descriptor parameters
echo "File Descriptors:"
echo "  fs.file-max = $(sysctl -n fs.file-max)"
echo "  fs.nr_open = $(sysctl -n fs.nr_open)"
echo ""

# Network parameters
echo "Network:"
echo "  net.core.somaxconn = $(sysctl -n net.core.somaxconn)"
echo "  net.core.netdev_max_backlog = $(sysctl -n net.core.netdev_max_backlog)"
echo "  net.ipv4.tcp_max_syn_backlog = $(sysctl -n net.ipv4.tcp_max_syn_backlog)"
echo "  net.core.rmem_max = $(sysctl -n net.core.rmem_max)"
echo "  net.core.wmem_max = $(sysctl -n net.core.wmem_max)"
echo ""

# Memory parameters
echo "Memory Management:"
echo "  vm.swappiness = $(sysctl -n vm.swappiness)"
echo "  vm.dirty_ratio = $(sysctl -n vm.dirty_ratio)"
echo "  vm.dirty_background_ratio = $(sysctl -n vm.dirty_background_ratio)"
echo "  vm.overcommit_memory = $(sysctl -n vm.overcommit_memory)"
echo ""

echo "=== Verification Complete ==="
EOF

chmod +x verify_sysctl.sh
Subtask 3.4: Testing the Complete Solution

Now let's test our complete solution:

# Run the temporary tuning script
echo "Testing temporary tuning..."
sudo ./system_tuning.sh

# Verify current settings
echo ""
echo "Verifying current settings..."
./verify_sysctl.sh

# Install persistent configuration
echo ""
echo "Installing persistent configuration..."
sudo ./install_sysctl_config.sh

# Final verification
echo ""
echo "Final verification..."
./verify_sysctl.sh
Subtask 3.5: Creating a Rollback Script

It's important to have a way to revert changes if needed:

cat > rollback_sysctl.sh << 'EOF'
#!/bin/bash

# Script to rollback sysctl changes

if [ "$EUID" -ne 0 ]; then
    echo "Please run this script as root or with sudo"
    exit 1
fi

echo "=== Rolling Back sysctl Configuration ==="
echo ""

# Remove our configuration file
if [ -f /etc/sysctl.d/99-performance.conf ]; then
    echo "Removing performance configuration..."
    rm /etc/sysctl.d/99-performance.conf
    echo "✓ Configuration file removed"
else
    echo "No performance configuration found"
fi

# Restore original configuration if backup exists
BACKUP_FILE=$(ls /etc/sysctl.conf.backup.* 2>/dev/null | tail -1)
if [ -n "$BACKUP_FILE" ]; then
    echo "Restoring original configuration from $BACKUP_FILE..."
    cp "$BACKUP_FILE" /etc/sysctl.conf
    echo "✓ Original configuration restored"
fi

# Reload default settings
echo "Reloading system defaults..."
sysctl -p
echo "✓ Default settings reloaded"

echo ""
echo "=== Rollback Complete ==="
echo "System has been restored to default configuration."
echo "Reboot recommended to ensure all changes take effect."
EOF

chmod +x rollback_sysctl.sh
