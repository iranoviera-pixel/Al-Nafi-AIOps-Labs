#!/bin/bash
NEW_HOSTNAME="lab-machine"
sudo hostnamectl set-hostname $NEW_HOSTNAME
echo "Hostname set to $NEW_HOSTNAME"

