#!/bin/bash

# Header
echo "File System Monitoring Report"
echo "-----------------------------"
date
echo

# Disk usage summary
echo "1. Overall Disk Usage:"
df -h --output=source,fstype,size,pcent,target | grep -v "tmpfs\|loop"

# Large partitions alert
echo -e "\n2. Partitions Over 80% Full:"
df -h | awk 'NR>1 && int($5) > 80 {print $1 " is " $5 " full"}'

# Inode usage
echo -e "\n3. Inode Usage:"
df -i | awk 'NR==1 || $5 > 0 {print}'
