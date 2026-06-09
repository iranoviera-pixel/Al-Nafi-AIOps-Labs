Lab 8: Writing a Shell Script for Directory Management

Objectives

By the end of this lab, you will be able to:

Write Bash scripts to automate directory management tasks.
Use conditional statements to check directory/file existence.
List, create, and organize files/directories programmatically.
Understand basic shell scripting syntax and best practices.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux commands (e.g., ls, mkdir, mv).
Access to a Linux terminal (Al Nafi’s cloud machine or any Linux distribution).
A text editor (e.g., nano, vim, or gedit).
Note: Al Nafi provides pre-configured Linux cloud instances. Click Start Lab to begin—no setup required!

Task 1: Create Directories if They Don’t Exist

Goal: Write a script to check if a directory exists and create it if it doesn’t.

Steps:

Open a terminal and create a new script file:
nano create_dir.sh
Add the following code:
#!/bin/bash

# Define directory name
dir_name="Lab8_Directory"

# Check if directory exists
if [ ! -d "$dir_name" ]; then
    mkdir "$dir_name"
    echo "Directory $dir_name created."
else
    echo "Directory $dir_name already exists."
fi
Save the file (Ctrl+O, then Enter) and exit (Ctrl+X).
Make the script executable:
chmod +x create_dir.sh
Run the script:
./create_dir.sh
Expected Output:

If Lab8_Directory doesn’t exist:
Directory Lab8_Directory created.
If it exists:
Directory Lab8_Directory already exists.
Troubleshooting:

If you get a "Permission denied" error, rerun chmod +x create_dir.sh.
Task 2: List Directories and Files in a Specific Path

Goal: Write a script to list all directories and files in a given path.

Steps:

Create a new script:
nano list_contents.sh
Add this code (replace /path/to/directory with your target path, e.g., ~/):
#!/bin/bash

echo "Enter a directory path:"
read path

echo "Directories in $path:"
ls -l "$path" | grep '^d'

echo "Files in $path:"
ls -l "$path" | grep -v '^d'
Save, make executable, and run:
chmod +x list_contents.sh
./list_contents.sh
Expected Output:

Enter a directory path:  
~/  
Directories in ~/:  
drwxr-xr-x 2 user user 4096 Jan 1 Documents  
...  
Files in ~/:  
-rw-r--r-- 1 user user  100 Jan 1 notes.txt  
...  
Key Concepts:

grep '^d' filters directory entries.
grep -v '^d' excludes directories.
Task 3: Move Files Based on Conditions

Goal: Write a script to move files to subdirectories by file type (e.g., .txt to a Text_Files folder).

Steps:

Create the script:
nano organize_files.sh
Add the code:
#!/bin/bash

# Create target directories
mkdir -p Text_Files Image_Files

# Move files based on extension
for file in *; do
    if [[ "$file" == *.txt ]]; then
        mv "$file" Text_Files/
    elif [[ "$file" == *.jpg || "$file" == *.png ]]; then
        mv "$file" Image_Files/
    fi
done

echo "Files organized!"
Save, make executable, and run:
chmod +x organize_files.sh
./organize_files.sh
Expected Outcome:

All .txt files move to Text_Files/.
All .jpg/.png files move to Image_Files/.
Troubleshooting:

If no files are moved, ensure the script is run in a directory with matching files.
