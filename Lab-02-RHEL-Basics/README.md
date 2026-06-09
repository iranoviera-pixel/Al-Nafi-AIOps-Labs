Lab 2: Basic Linux Commands (ls, cp, chmod, grep)

Objectives

By the end of this lab, students will be able to:

List and navigate directory contents using ls.
Copy files and directories using cp.
Modify file permissions with chmod.
Search for text patterns in files using grep.
Automate basic tasks using a simple shell script.
Prerequisites

Before starting this lab, ensure you have:

Access to a Linux environment: Al Nafi provides pre-configured cloud machines. Click Start Lab to launch your Linux instance.
Basic familiarity with the terminal: Know how to open a terminal and execute commands.
A text editor: Use nano, vim, or any preferred editor for writing scripts.
Lab Setup

Launch your cloud machine:

Click Start Lab on the Al Nafi platform.
Wait for the machine to initialize (usually takes 1 minute).
Open the terminal window once the machine is ready.
Verify your environment:

whoami  # Should display your username
pwd     # Should show your current directory (e.g., /home/user)
Task 1: List Directory Contents with ls

Objective: Learn to list files and directories.

Steps:

List files in the current directory:

ls
Expected Output: Displays all files and folders in your current directory.
List files with details (permissions, size, etc.):

ls -l
Explanation: The -l flag shows a detailed ("long") listing.
List hidden files (files starting with .):

ls -a
Key Concept: Hidden files are typically configuration files.
Combine flags for detailed hidden files:

ls -la
Task 2: Copy Files with cp

Objective: Copy files and directories.

Steps:

Create a test file:

echo "Hello, Linux!" > original.txt
Copy the file:

cp original.txt copy.txt
Verify: Run ls to see both files.
Copy a directory recursively:

mkdir mydir
cp -r mydir mydir_backup  # -r flag copies directories
Task 3: Modify Permissions with chmod

Objective: Change file permissions for security.

Steps:

Check current permissions:

ls -l original.txt
Output Example: -rw-r--r-- 1 user group 13 Jan 1 10:00 original.txt
Make the file executable:

chmod +x original.txt
Verify: Run ls -l again. The permissions should now include x (e.g., -rwxr-xr-x).
Set specific permissions (numeric mode):

chmod 755 original.txt  # Owner: read/write/execute, Others: read/execute
Task 4: Search Text with grep

Objective: Find patterns in files.

Steps:

Create a sample file:

echo -e "apple\nbanana\ncherry\ndate" > fruits.txt
Search for a pattern:

grep "banana" fruits.txt
Expected Output: banana
Case-insensitive search:

grep -i "APPLE" fruits.txt
Search in multiple files:

grep "Hello" *.txt  # Searches all .txt files for "Hello"
Task 5: Automate Tasks with a Shell Script

Objective: Write a script to combine the above commands.

Steps:

Create a script file:

nano my_script.sh
Add the following code:

#!/bin/bash
echo "Listing files:"
ls -l
echo "Copying original.txt to backup.txt..."
cp original.txt backup.txt
echo "Making backup.txt executable..."
chmod +x backup.txt
echo "Searching for 'Hello' in files:"
grep "Hello" *.txt
Save and exit (Ctrl+O, Enter, Ctrl+X in nano).

Run the script:

bash my_script.sh
Troubleshooting: If you get a "permission denied" error, run chmod +x my_script.sh first.
