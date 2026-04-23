# Lab 21: System Maintenance via Single-User Mode

This repository documents the process of performing critical system maintenance on an Ubuntu-based system by booting into Single-User Mode (Rescue Mode).

## Objectives
* Gain root access without a standard login.
* Perform filesystem consistency checks.
* Manage administrative credentials and repair broken packages.

## Technical Workflow

### 1. Accessing the Bootloader (GRUB)
* Modified `/etc/default/grub` to set `GRUB_TIMEOUT=10` for easier access.
* Intercepted the boot process and entered the GRUB editor by pressing `e` on the Ubuntu entry.
* Appended the `single` parameter to the end of the `linux` kernel line to initiate Rescue Mode.

### 2. Filesystem Repair (fsck)
* Identified the primary partition using `mount`.
* Executed the following command to repair the filesystem:
  ```bash
  fsck -y /dev/sda1

