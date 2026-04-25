#!/bin/bash

# Function to clean temporary files
clean_temp_files() {
    echo "Cleaning temporary files..."
    sudo rm -rf /tmp/*
    echo "Temporary files cleaned."
}

# Function to monitor and kill high-CPU processes
monitor_processes() {
    echo "Monitoring processes..."
    top -bn1 | head -n 10
    read -p "Kill a process? Enter PID (or 0 to skip): " pid
    if [ "$pid" -ne 0 ]; then
        sudo kill -9 "$pid"
        echo "Process $pid terminated."
    fi
}

# Function to backup logs
backup_logs() {
    echo "Backing up system logs..."
    backup_dir="/var/log/backup_$(date +%Y%m%d)"
    sudo mkdir -p "$backup_dir"
    sudo cp /var/log/syslog* "$backup_dir"
    echo "Logs backed up to $backup_dir."
}

# Main menu
while true; do
    echo "1. Clean Temp Files | 2. Monitor Processes | 3. Backup Logs | 4. Exit"
    read -p "Choose an option: " choice
    case $choice in
        1) clean_temp_files ;;
        2) monitor_processes ;;
        3) backup_logs ;;
        4) exit 0 ;;
        *) echo "Invalid option." ;;
    esac
done
