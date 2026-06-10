#!/bin/bash
HOSTS=("8.8.8.8" "google.com" "localhost")

for host in "${HOSTS[@]}"; do
    echo "Checking connectivity to $host..."
    ping -c 2 "$host" >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "$host is reachable."
    else
        echo "$host is unreachable."
    fi
done

