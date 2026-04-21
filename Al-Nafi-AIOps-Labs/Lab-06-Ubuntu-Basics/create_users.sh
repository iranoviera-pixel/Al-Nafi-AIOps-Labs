#!/bin/bash
# Script to create users and assign permissions
sudo useradd -m -s /bin/bash user1
sudo passwd user1  # Set password when prompted)
sudo mkdir /home/user1/data
sudo chown user1:user1 /home/user1/data
sudo chmod 750 /home/user1/data

