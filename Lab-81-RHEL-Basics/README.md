Lab 81: Setting Up KVM and libvirt

Objectives

By the end of this lab, you will be able to:

Install and configure KVM (Kernel-based Virtual Machine) and libvirt on CentOS
Verify KVM installation and hardware virtualization support
Create and manage virtual machines using virsh command-line tools
Write automation scripts for virtual machine deployment
Understand the fundamentals of virtualization management with open-source tools
Prerequisites

Before starting this lab, you should have:

Basic knowledge of Linux command line operations
Understanding of system administration concepts
Familiarity with text editors like vi/vim or nano
Basic networking concepts
Root or sudo access to a CentOS system
Note: Al Nafi provides ready-to-use Linux-based cloud machines for this lab. Simply click "Start Lab" to begin - no need to build your own VM infrastructure.

Lab Environment Setup

This lab uses CentOS 8/9 with the following specifications:

Minimum 4GB RAM
At least 20GB free disk space
CPU with virtualization support (Intel VT-x or AMD-V)
Network connectivity for package installation
Task 1: Install and Configure KVM and libvirt on CentOS

Subtask 1.1: Update System and Check Hardware Support

First, let's ensure our system is up-to-date and check if our hardware supports virtualization.

# Update the system packages
sudo dnf update -y

# Check if CPU supports virtualization
egrep -c '(vmx|svm)' /proc/cpuinfo
If the output is greater than 0, your CPU supports virtualization. If it returns 0, virtualization may be disabled in BIOS.

# Check if virtualization is enabled in BIOS
lscpu | grep Virtualization
Subtask 1.2: Install KVM and Related Packages

Install the necessary packages for KVM virtualization:

# Install KVM and virtualization packages
sudo dnf groupinstall "Virtualization Host" -y

# Install additional useful packages
sudo dnf install -y virt-install virt-viewer virt-manager libguestfs-tools
Subtask 1.3: Start and Enable libvirt Services

Enable and start the libvirt daemon:

# Start libvirtd service
sudo systemctl start libvirtd

# Enable libvirtd to start at boot
sudo systemctl enable libvirtd

# Check service status
sudo systemctl status libvirtd
Subtask 1.4: Configure User Permissions

Add your user to the libvirt group to manage VMs without sudo:

# Add current user to libvirt group
sudo usermod -aG libvirt $USER

# Add user to kvm group
sudo usermod -aG kvm $USER

# Apply group changes (logout and login, or use newgrp)
newgrp libvirt
Task 2: Verify KVM Installation

Subtask 2.1: Check KVM Module Loading

Verify that KVM modules are loaded:

# Check if KVM modules are loaded
lsmod | grep kvm

# For Intel processors, you should see kvm_intel
# For AMD processors, you should see kvm_amd
Subtask 2.2: Verify libvirt Installation

Test libvirt connectivity:

# Test libvirt connection
virsh list --all

# Check libvirt version
virsh version

# Display system information
virsh nodeinfo
Subtask 2.3: Check Available Storage Pools

List and examine default storage pools:

# List storage pools
virsh pool-list --all

# Get details about default pool
virsh pool-info default

# Check pool path
virsh pool-dumpxml default
Subtask 2.4: Verify Network Configuration

Check default network configuration:

# List virtual networks
virsh net-list --all

# Show default network details
virsh net-info default

# Display network configuration
virsh net-dumpxml default
Task 3: Create and Manage Virtual Machines Using virsh

Subtask 3.1: Download a Linux ISO

Download a lightweight Linux distribution for testing:

# Create directory for ISOs
sudo mkdir -p /var/lib/libvirt/images/iso

# Download CentOS Stream 9 minimal ISO (or use wget)
cd /var/lib/libvirt/images/iso
sudo wget https://mirror.stream.centos.org/9-stream/BaseOS/x86_64/iso/CentOS-Stream-9-latest-x86_64-boot.iso

# Alternatively, download Alpine Linux (smaller, faster)
sudo wget https://dl-cdn.alpinelinux.org/alpine/v3.18/releases/x86_64/alpine-standard-3.18.4-x86_64.iso
Subtask 3.2: Create Your First Virtual Machine

Create a virtual machine using virt-install:

# Create a VM with Alpine Linux
sudo virt-install \
  --name alpine-test \
  --ram 1024 \
  --disk path=/var/lib/libvirt/images/alpine-test.qcow2,size=10,format=qcow2 \
  --vcpus 1 \
  --os-variant alpinelinux3.18 \
  --network bridge=virbr0 \
  --graphics none \
  --console pty,target_type=serial \
  --cdrom /var/lib/libvirt/images/iso/alpine-standard-3.18.4-x86_64.iso \
  --boot cdrom
Subtask 3.3: Basic VM Management Commands

Learn essential virsh commands for VM management:

# List all VMs
virsh list --all

# Start a VM
virsh start alpine-test

# Connect to VM console
virsh console alpine-test
# (Press Ctrl+] to exit console)

# Shutdown VM gracefully
virsh shutdown alpine-test

# Force stop VM
virsh destroy alpine-test

# Get VM information
virsh dominfo alpine-test

# Edit VM configuration
virsh edit alpine-test
Subtask 3.4: VM Snapshot Management

Create and manage VM snapshots:

# Create a snapshot
virsh snapshot-create-as alpine-test snapshot1 "Initial setup complete"

# List snapshots
virsh snapshot-list alpine-test

# Revert to snapshot
virsh snapshot-revert alpine-test snapshot1

# Delete snapshot
virsh snapshot-delete alpine-test snapshot1
Task 4: Write a Script to Automate VM Setup

Subtask 4.1: Create VM Creation Script

Create a comprehensive script to automate VM creation:

# Create the script file
nano ~/create-vm.sh
Add the following content to the script:

#!/bin/bash

# VM Creation Automation Script
# Usage: ./create-vm.sh <vm-name> <ram-mb> <disk-gb> <iso-path>

set -e  # Exit on any error

# Function to display usage
usage() {
    echo "Usage: $0 <vm-name> <ram-mb> <disk-gb> <iso-path>"
    echo "Example: $0 test-vm 2048 20 /path/to/iso/file.iso"
    exit 1
}

# Check if correct number of arguments provided
if [ $# -ne 4 ]; then
    usage
fi

# Assign variables
VM_NAME=$1
RAM_MB=$2
DISK_GB=$3
ISO_PATH=$4

# Configuration
DISK_PATH="/var/lib/libvirt/images/${VM_NAME}.qcow2"
VCPUS=2
OS_VARIANT="generic"

# Validate inputs
if [ $RAM_MB -lt 512 ]; then
    echo "Error: RAM must be at least 512MB"
    exit 1
fi

if [ $DISK_GB -lt 5 ]; then
    echo "Error: Disk size must be at least 5GB"
    exit 1
fi

if [ ! -f "$ISO_PATH" ]; then
    echo "Error: ISO file not found: $ISO_PATH"
    exit 1
fi

# Check if VM already exists
if virsh list --all | grep -q "$VM_NAME"; then
    echo "Error: VM '$VM_NAME' already exists"
    exit 1
fi

echo "Creating VM: $VM_NAME"
echo "RAM: ${RAM_MB}MB"
echo "Disk: ${DISK_GB}GB"
echo "ISO: $ISO_PATH"
echo "Disk Path: $DISK_PATH"

# Create the virtual machine
virt-install \
    --name "$VM_NAME" \
    --ram "$RAM_MB" \
    --disk path="$DISK_PATH",size="$DISK_GB",format=qcow2 \
    --vcpus "$VCPUS" \
    --os-variant "$OS_VARIANT" \
    --network bridge=virbr0 \
    --graphics none \
    --console pty,target_type=serial \
    --cdrom "$ISO_PATH" \
    --boot cdrom \
    --noautoconsole

echo "VM '$VM_NAME' created successfully!"
echo "To connect to the console: virsh console $VM_NAME"
echo "To start the VM: virsh start $VM_NAME"
Subtask 4.2: Make Script Executable and Test

# Make script executable
chmod +x ~/create-vm.sh

# Test the script (adjust paths as needed)
./create-vm.sh test-vm 1024 10 /var/lib/libvirt/images/iso/alpine-standard-3.18.4-x86_64.iso
Subtask 4.3: Create VM Management Script

Create a comprehensive VM management script:

# Create management script
nano ~/manage-vm.sh
Add the following content:

#!/bin/bash

# VM Management Script
# Provides easy interface for common VM operations

set -e

# Function to display menu
show_menu() {
    echo "=== VM Management Menu ==="
    echo "1. List all VMs"
    echo "2. Start VM"
    echo "3. Stop VM"
    echo "4. Restart VM"
    echo "5. Delete VM"
    echo "6. VM Information"
    echo "7. Create Snapshot"
    echo "8. List Snapshots"
    echo "9. Connect to Console"
    echo "0. Exit"
    echo "=========================="
}

# Function to list VMs
list_vms() {
    echo "All Virtual Machines:"
    virsh list --all
}

# Function to start VM
start_vm() {
    read -p "Enter VM name to start: " vm_name
    if virsh list --all | grep -q "$vm_name"; then
        virsh start "$vm_name"
        echo "VM '$vm_name' started successfully"
    else
        echo "VM '$vm_name' not found"
    fi
}

# Function to stop VM
stop_vm() {
    read -p "Enter VM name to stop: " vm_name
    read -p "Graceful shutdown? (y/n): " graceful
    
    if [ "$graceful" = "y" ]; then
        virsh shutdown "$vm_name"
        echo "Graceful shutdown initiated for '$vm_name'"
    else
        virsh destroy "$vm_name"
        echo "VM '$vm_name' forcefully stopped"
    fi
}

# Function to restart VM
restart_vm() {
    read -p "Enter VM name to restart: " vm_name
    virsh reboot "$vm_name"
    echo "VM '$vm_name' restarted"
}

# Function to delete VM
delete_vm() {
    read -p "Enter VM name to delete: " vm_name
    read -p "Are you sure? This will delete the VM and its disk! (yes/no): " confirm
    
    if [ "$confirm" = "yes" ]; then
        # Stop VM if running
        virsh destroy "$vm_name" 2>/dev/null || true
        # Undefine VM and remove disk
        virsh undefine "$vm_name" --remove-all-storage
        echo "VM '$vm_name' deleted successfully"
    else
        echo "Operation cancelled"
    fi
}

# Function to show VM info
vm_info() {
    read -p "Enter VM name: " vm_name
    virsh dominfo "$vm_name"
}

# Function to create snapshot
create_snapshot() {
    read -p "Enter VM name: " vm_name
    read -p "Enter snapshot name: " snap_name
    read -p "Enter description: " description
    
    virsh snapshot-create-as "$vm_name" "$snap_name" "$description"
    echo "Snapshot '$snap_name' created for VM '$vm_name'"
}

# Function to list snapshots
list_snapshots() {
    read -p "Enter VM name: " vm_name
    virsh snapshot-list "$vm_name"
}

# Function to connect to console
connect_console() {
    read -p "Enter VM name: " vm_name
    echo "Connecting to console... (Press Ctrl+] to exit)"
    virsh console "$vm_name"
}

# Main menu loop
while true; do
    show_menu
    read -p "Select option (0-9): " choice
    
    case $choice in
        1) list_vms ;;
        2) start_vm ;;
        3) stop_vm ;;
        4) restart_vm ;;
        5) delete_vm ;;
        6) vm_info ;;
        7) create_snapshot ;;
        8) list_snapshots ;;
        9) connect_console ;;
        0) echo "Goodbye!"; exit 0 ;;
        *) echo "Invalid option. Please try again." ;;
    esac
    
    echo
    read -p "Press Enter to continue..."
    clear
done
Subtask 4.4: Test Management Script

# Make management script executable
chmod +x ~/manage-vm.sh

# Run the management script
./manage-vm.sh
