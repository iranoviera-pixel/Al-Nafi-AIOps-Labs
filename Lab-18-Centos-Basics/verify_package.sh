#!/bin/bash

# Check if package name is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <package-name>"
    exit 1
fi

PACKAGE=$1

# Check if package is installed
if rpm -q $PACKAGE &>/dev/null; then
    echo "$PACKAGE is installed."
    # Get installed version
    INSTALLED_VERSION=$(rpm -q --queryformat '%{VERSION}' $PACKAGE)
    echo "Installed version: $INSTALLED_VERSION"

    # Check for updates (requires internet)
    echo "Checking for updates..."
    yum info available $PACKAGE | grep -A1 "Available Packages"
else
    echo "$PACKAGE is NOT installed."
fi

