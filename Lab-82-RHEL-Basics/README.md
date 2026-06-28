Lab 82: Using virt-manager and virsh

Objectives

By the end of this lab, you will be able to:

Install and configure virt-manager for managing virtual machines (VMs).
Create a VM using virt-manager's graphical interface.
Use virsh commands to manage VM lifecycle operations (start, stop, restart).
Write a Bash script to automate basic VM management tasks.
Prerequisites

Before starting, ensure you have:

A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with Linux terminal commands.
Administrative (sudo) privileges for package installation.
Task 1: Install virt-manager and Configure It

Step 1: Update Package Repositories

Open a terminal and run:

sudo apt update
Step 2: Install Required Packages

Install virt-manager, libvirt, and dependencies:

sudo apt install -y virt-manager qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils
Step 3: Verify Installation

Check if the libvirtd service is running:

sudo systemctl status libvirtd
Expected Output:
Active: active (running) indicates success.

Step 4: Add User to libvirt Group

Allow your user to manage VMs:

sudo usermod -aG libvirt $(whoami)
sudo usermod -aG kvm $(whoami)
Note: Log out and back in for changes to take effect.

Task 2: Create a VM Using virt-manager

Step 1: Launch virt-manager

Run:

virt-manager
Step 2: Create a New VM

Click File > New Virtual Machine.
Select Local install media (ISO) and browse to your OS ISO (e.g., Ubuntu 22.04).
Allocate RAM (e.g., 2GB) and CPUs (e.g., 2 cores).
Create a disk image (e.g., 20GB, QCow2 format).
Name the VM (e.g., lab-vm) and finish setup.
Step 3: Start the VM

In virt-manager, right-click the VM and select Run.

Troubleshooting:

If the VM fails to start, check /var/log/libvirt/qemu/lab-vm.log for errors.
Task 3: Manage VM Lifecycle with virsh

Step 1: List VMs

virsh list --all
Expected Output:
Lists all VMs (e.g., lab-vm in "shut off" or "running" state).

Step 2: Start/Stop/Restart a VM

virsh start lab-vm       # Start
virsh shutdown lab-vm    # Graceful stop
virsh destroy lab-vm     # Force stop (unclean)
virsh reboot lab-vm      # Restart
Step 3: View VM Information

virsh dominfo lab-vm
Expected Output:
Displays CPU, memory, and state details.

Task 4: Automate VM Management with a Script

Step 1: Create a Script

Open a file named vm_manager.sh:

#!/bin/bash
VM_NAME="lab-vm"

case "$1" in
    start)
        virsh start "$VM_NAME"
        echo "Started $VM_NAME"
        ;;
    stop)
        virsh shutdown "$VM_NAME"
        echo "Stopped $VM_NAME"
        ;;
    status)
        virsh list --all | grep "$VM_NAME"
        ;;
    *)
        echo "Usage: $0 {start|stop|status}"
        exit 1
esac
Step 2: Make the Script Executable

chmod +x vm_manager.sh
Step 3: Test the Script

./vm_manager.sh start   # Starts the VM
./vm_manager.sh status  # Checks status
