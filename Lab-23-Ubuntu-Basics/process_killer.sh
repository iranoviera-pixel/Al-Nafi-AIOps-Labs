#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <process_name>"
    exit 1
fi

echo "Searching for processes containing: $1"
pgrep -l "$1"

read -p "Kill these processes? (y/n) " answer

if [ "$answer" = "y" ]; then
    pkill "$1"
    echo "Processes terminated."
else
    echo "Operation cancelled."
fi


