#!/bin/bash
# List of packages to remove
PACKAGES="httpd mariadb-server php"

for pkg in $PACKAGES; do
    sudo yum remove -y "$pkg"
done


