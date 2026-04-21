#!/bin/bash

PACKAGE_NAME="$1"
LOG_FILE="/var/log/package_install.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Install using YUM
log_message "Attempting to install $PACKAGE_NAME using YUM..."
if sudo yum install -y "$PACKAGE_NAME" &>> "$LOG_FILE"; then
    log_message "SUCCESS: $PACKAGE_NAME installed via YUM."
else
    log_message "ERROR: YUM installation failed. Trying RPM..."

    # Install using RPM (assuming the package RPM is in /tmp)
    RPM_FILE="/tmp/${PACKAGE_NAME}.rpm"
    if [ -f "$RPM_FILE" ]; then
        if sudo rpm -ivh "$RPM_FILE" &>> "$LOG_FILE"; then
            log_message "SUCCESS: $PACKAGE_NAME installed via RPM."
        else
            log_message "ERROR: RPM installation failed. Check dependencies."
        fi
    else
        log_message "ERROR: RPM file $RPM_FILE not found."
    fi
fi


