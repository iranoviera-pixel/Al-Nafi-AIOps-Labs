#!/bin/bash

# Variables
USER="your_username"
KEY_FILE="$HOME/.ssh/id_rsa.pub"

# Check if key exists
if [ ! -f "$KEY_FILE" ]; then
    echo "SSH key not found at $KEY_FILE"
    exit 1
fi

# Read server list
while read -r server; do
    echo "Deploying to $server..."
    
    # Check if server is reachable
    if ping -c 1 "$server" &> /dev/null; then
        # Copy key
        ssh-copy-id -i "$KEY_FILE" "$USER@$server"
        
        # Verify
        ssh -o PasswordAuthentication=no "$USER@$server" echo "Successfully connected to $server"
    else
        echo "$server is unreachable"
    fi
done < server_list.txt

echo "Deployment complete"


