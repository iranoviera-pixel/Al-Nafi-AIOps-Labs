#!/bin/bash

# Check for root privileges
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root." >&2
    exit 1
fi

# Prompt for username and permission level
read -p "Enter username: " username
read -p "Grant full sudo access? (y/n): " full_access

if [ "$full_access" = "y" ]; then
    echo "$username ALL=(ALL:ALL) ALL" >> /etc/sudoers
    echo "Full sudo access granted to $username."
else
    read -p "Enter allowed commands (comma-separated): " commands
    echo "$username ALL=(ALL) $commands" >> /etc/sudoers
    echo "Custom sudo access granted to $username for: $commands."
fi


