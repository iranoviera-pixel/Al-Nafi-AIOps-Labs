#!/bin/bash

echo "Enter the package name to search:"
read search_term

if [ -z "$search_term" ]; then
    echo "Error: No input provided."
    exit 1
fi

echo "Choose an option:"
echo "1. Search for packages"
echo "2. Show detailed package info"
read option

case $option in
    1) yum search "$search_term" ;;
    2) yum info "$search_term" ;;
    *) echo "Invalid option." ;;
esac



