Lab 1: Understanding the Linux Filesystem Hierarchy

Objectives

By the end of this lab, students will be able to:

Identify and explain the purpose of key directories in the Linux filesystem hierarchy.
Use the ls command to explore directory contents.
Write and execute a basic Bash script to automate directory listing.
Prerequisites

Before starting this lab, ensure you have:

Access to a Linux environment: Use the provided Al Nafi cloud machine (click Start Lab to launch).
Basic Linux command-line knowledge: Understand how to open a terminal and run simple commands like cd and ls.
A text editor: Use nano or vim (pre-installed in the cloud machine).
Lab Setup

Launch the Cloud Machine:
Click Start Lab in your Al Nafi dashboard to access a pre-configured Linux environment.
Open a Terminal:
Press Ctrl + Alt + T or search for "Terminal" in the applications menu.
Task 1: Research Key Linux Directories

Subtasks

Understand the Filesystem Hierarchy Standard (FHS):
Linux organizes files in a standardized directory structure. Below are key directories and their purposes:

Directory	Purpose
/	Root directory (base of the filesystem).
/bin	Essential user binaries (e.g., ls, cp).
/etc	System configuration files (e.g., /etc/passwd).
/home	User home directories (e.g., /home/student).
/var	Variable data (e.g., logs in /var/log).
/tmp	Temporary files (cleared on reboot).
Explore Directories:
Run the following commands to list contents and observe outputs:

ls /bin       # Lists core system commands
ls /etc       # Shows configuration files
ls /home      # Displays user directories
Expected Output:
A list of files/subdirectories for each path.

Task 2: List Directory Contents with ls

Subtasks

Basic Listing:

ls /          # Lists all top-level directories
Expected Output:
Directories like bin, etc, home, etc.

Detailed View:
Use flags for more information:

ls -l /var    # Shows permissions, size, and modification time
ls -a /home   # Includes hidden files (names start with '.')
Troubleshooting:

If you see Permission denied, prepend sudo (admin rights required for some directories).
Task 3: Write a Script to List All Directories Under /

Subtasks

Create a Script:
Open a text editor and write:

#!/bin/bash
echo "Listing all directories under /:"
for dir in /*; do
  if [ -d "$dir" ]; then
    echo "Directory: $dir"
    ls -l "$dir"
  fi
done
Save and Execute:

Save as list_dirs.sh.
Make it executable:
chmod +x list_dirs.sh
Run the script:
./list_dirs.sh
Expected Output:
A list of all directories under / with their contents.
