#!/bin/bash

# Input file containing package names
PACKAGE_FILE="packages.txt"

# Check if the file exists
if [ ! -f "$PACKAGE_FILE" ]; then
    echo "Error: $PACKAGE_FILE not found."
    exit 1
fi

# Read packages from the file
while IFS= read -r package; do
    # Install the package
    echo "Installing $package..."
    sudo yum install -y "$package"

    # Update the package (if already installed)
    echo "Updating $package..."
    sudo yum update -y "$package"

    # Remove the package (optional: uncomment if needed)
    # echo "Removing $package..."
    # sudo yum remove -y "$package"
done < "$PACKAGE_FILE"


