#!/usr/bin/env python3
import os
import shutil
import subprocess
from datetime import datetime

def clean_temp_files():
    print("Cleaning temporary files...")
    os.system("sudo rm -rf /tmp/*")
    print("Done.")

def monitor_processes():
    print("Running top command...")
    subprocess.run(["top", "-bn1"])

def backup_logs():
    backup_dir = f"/var/log/backup_{datetime.now().strftime('%Y%m%d')}"
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy2("/var/log/syslog", backup_dir)
    print(f"Logs backed up to {backup_dir}")

if __name__ == "__main__":
    while True:
        print("1. Clean Temp Files\n2. Monitor Processes\n3. Backup Logs\n4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            clean_temp_files()
        elif choice == "2":
            monitor_processes()
        elif choice == "3":
            backup_logs()
        elif choice == "4":
            break


