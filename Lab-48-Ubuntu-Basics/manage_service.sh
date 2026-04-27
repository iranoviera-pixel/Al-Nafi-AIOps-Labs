#!/bin/bash
SERVICE_NAME=$1
ACTION=$2

if [ "$ACTION" == "start" ]; then
    sudo systemctl start $SERVICE_NAME
    echo "Started $SERVICE_NAME"
elif [ "$ACTION" == "stop" ]; then
    sudo systemctl stop $SERVICE_NAME
    echo "Stopped $SERVICE_NAME"
else
    echo "Usage: ./manage_service.sh <service_name> <start|stop>"
fi
