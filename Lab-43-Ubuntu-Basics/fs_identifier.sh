#!/bin/bash
echo "File System Types on This System:"
echo "--------------------------------"
lsblk -f | awk 'NR>1 && $2 != "" {print $1 " - " $2}'


