#!/bin/bash

# Define output file
OUTPUT_FILE="system_report_$(date +%Y\%m\%d_%H\%M\%S).csv"

# Header for CSV
echo "Timestamp,CPU(%),Memory(%),Disk(%),Load Average" > $OUTPUT_FILE

# Collect data every 5 seconds, 6 times (30 seconds total)
for i in {1..6}; do
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
    CPU=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
    MEM=$(free | grep Mem | awk '{print $3/$2 * 100.0}')
    DISK=$(df -h | grep "/dev/sda1" | awk '{print $5}' | tr -d '%')
    LOAD=$(uptime | awk -F 'load average:' '{print $2}' | xargs)
    
    # Append to CSV
    echo "$TIMESTAMP,$CPU,$MEM,$DISK,$LOAD" >> $OUTPUT_FILE
    sleep 5
done

echo "Report generated: $OUTPUT_FILE"


