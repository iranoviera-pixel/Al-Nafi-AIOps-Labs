#!/bin/bash

echo "Current process priorities:"
ps -eo pid,ni,cmd | head -n 5

read -p "Enter PID to renice: " pid
read -p "Enter new nice value (-20 to 19): " niceval

if ! sudo renice -n $niceval -p $pid; then
    echo "Failed to change priority. Try with sudo?"
fi
    echo "Priority changed successfully for PID $pid"
fi


