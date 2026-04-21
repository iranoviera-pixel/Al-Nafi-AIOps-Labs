#!/bin/bash

# Check if a package name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <package_name>"
    exit 1
fi

# Install the package and dependencies
sudo yum install -y "$1"

# Check if installation was successful
if [ $? -eq 0 ]; then
    echo "Package '$1' and its dependencies installed successfully."
else
    echo "Failed to install package '$1'."
fi


