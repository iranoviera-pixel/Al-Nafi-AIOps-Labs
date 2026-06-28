Lab 84: Virtual Storage Configuration for KVM

Objectives

By the end of this lab, students will be able to:

Create and manage virtual storage disks using qemu-img.
Attach virtual storage to KVM virtual machines using virsh.
Automate storage allocation and attachment using a Bash script.
Prerequisites

Before starting, ensure you have:

A Linux-based system with KVM/QEMU installed (provided by Al Nafi's cloud lab).
Basic familiarity with Linux command-line operations.
A running KVM virtual machine (VM) for testing (create one using virt-install if needed).
Task 1: Create Virtual Storage Using qemu-img

Step 1: Check Available Storage

Run the following command to list existing storage pools:

virsh pool-list
Expected Output:
A table showing active/inactive storage pools (e.g., default).

Step 2: Create a Raw Disk Image

Use qemu-img to create a 10GB disk image in /var/lib/libvirt/images/:

sudo qemu-img create -f raw /var/lib/libvirt/images/vm-disk2.raw 10G
Explanation:

-f raw: Specifies the disk format (raw is simplest for beginners).
10G: Allocates 10GB of space.
Verify Creation:

ls -lh /var/lib/libvirt/images/vm-disk2.raw
Expected Output:

-rw-r--r-- 1 root root 10G [timestamp] vm-disk2.raw
Troubleshooting:

If permission denied, prepend sudo or ensure your user is in the libvirt group.
Task 2: Attach Storage to a VM Using virsh

Step 1: Identify the Target VM

List running VMs:

virsh list --all
Note the VM name (e.g., ubuntu-vm).

Step 2: Attach the Disk

Attach the disk to the VM as a storage device:

virsh attach-disk ubuntu-vm /var/lib/libvirt/images/vm-disk2.raw vdb --persistent
Explanation:

vdb: Assigns the disk as /dev/vdb in the VM.
--persistent: Ensures the disk remains attached after reboot.
Verify Attachment:

Connect to the VM:
virsh console ubuntu-vm
Inside the VM, check disks:
lsblk
Expected Output:

vdb     252:16   0   10G  0 disk
Troubleshooting:

If the disk doesn’t appear, restart the VM:
virsh reboot ubuntu-vm
Task 3: Automate Storage Allocation with a Script

Step 1: Create a Bash Script

Write a script (attach-storage.sh) to automate disk creation/attachment:

#!/bin/bash
VM_NAME=$1
DISK_SIZE=$2
DISK_PATH="/var/lib/libvirt/images/${VM_NAME}-additional-disk.raw"

# Create disk
sudo qemu-img create -f raw $DISK_PATH $DISK_SIZE

# Attach disk
virsh attach-disk $VM_NAME $DISK_PATH vdb --persistent

echo "Disk $DISK_PATH attached to $VM_NAME as /dev/vdb"
Step 2: Make the Script Executable

chmod +x attach-storage.sh
Step 3: Run the Script

./attach-storage.sh ubuntu-vm 5G
Expected Outcome:
A 5GB disk is created and attached to ubuntu-vm.
