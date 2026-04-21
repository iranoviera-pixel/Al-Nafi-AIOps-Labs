#!/bin/bash
# Backup script for Lab 3
BACKUP_DIR="./backups"
SOURCE_DIR="./"
mkdir -p $BACKUP_DIR
tar -czvf "$BACKUP_DIR/backup_$(date +%Y%m%d).tar.gz" $SOURCE_DIR/*.txt $SOURCE_DIR/*.log
echo "Backup completed. Files saved in $BACKUP_DIR."

