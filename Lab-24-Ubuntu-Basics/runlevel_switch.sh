#!/bin/bash
HOUR=$(date +%H)
if [ $HOUR -ge 22 ] || [ $HOUR -lt 6 ]; then
    sudo systemctl isolate multi-user.target
else
    sudo systemctl isolate graphical.target
fi


