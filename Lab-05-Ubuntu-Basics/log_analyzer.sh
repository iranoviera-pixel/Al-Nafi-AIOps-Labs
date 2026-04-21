#!/bin/bash
LOG_FILE="/var/log/syslog"
ERROR_KEYWORDS=("error" "failed" "warning")

echo "Scanning $LOG_FILE for errors..."
for keyword in "${ERROR_KEYWORDS[@]}"; do
    echo "=== $keyword ==="
    grep -i "$keyword" "$LOG_FILE"
done
