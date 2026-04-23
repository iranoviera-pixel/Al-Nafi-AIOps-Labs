#!/bin/bash
# Script to automate updates and package installation

echo "Starting system update..."
sudo yum update -y

read -p "Enter a package to install: " package
sudo yum install $package -y

echo "Verifying installation..."
which $package


