#!/bin/bash

PACKAGES="bash httpd nginx"

for pkg in $PACKAGES; do
    echo "Verifying $pkg..."
    rpm -V $pkg
done


