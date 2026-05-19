#!/bin/bash
# Install NFS client
sudo apt update && sudo apt install nfs-common -y

# Create mount point and mount
sudo mkdir -p /mnt/client_share
sudo mount $1:/mnt/nfs_share /mnt/client_share

# Add to fstab for persistence
echo "$1:/mnt/nfs_share /mnt/client_share nfs defaults 0 0" | sudo tee -a /etc/fstab
