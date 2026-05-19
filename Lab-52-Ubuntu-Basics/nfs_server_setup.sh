#!/bin/bash
# Install NFS server
sudo apt update && sudo apt install nfs-kernel-server -y

# Create and configure share
sudo mkdir -p /mnt/nfs_share
sudo chown nobody:nogroup /mnt/nfs_share
echo "/mnt/nfs_share $1(rw,sync,no_subtree_check)" | sudo tee -a /etc/exports

# Restart NFS
sudo exportfs -a
sudo systemctl restart nfs-kernel-server
