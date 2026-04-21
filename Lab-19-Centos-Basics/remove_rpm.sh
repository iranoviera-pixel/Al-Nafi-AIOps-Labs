#!/bin/bash
# List of packages to remove
PACKAGES="vim-enhanced nano"

for pkg in $PACKAGES; do
    sudo rpm -e "$pkg"
done


