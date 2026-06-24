Lab 61: Advanced Bash Functions and Error Handling

Objectives

By the end of this lab, you will be able to:

Write reusable Bash functions for file manipulation tasks.
Implement error handling using trap, exit, and return.
Create a script that logs errors based on command exit statuses.
Understand how to debug and troubleshoot Bash scripts.
Prerequisites

Before starting, ensure you have:

Basic knowledge of Linux commands and Bash scripting.
Access to a Linux-based system (Al Nafi provides ready-to-use cloud machines—click Start Lab to begin).
A text editor (e.g., nano, vim, or gedit).
Task 1: Write Bash Functions for File Manipulation

Step 1: Create a Simple Function

We’ll start by writing a function to create a directory and a file inside it.

#!/bin/bash

# Function to create a directory and a file
create_dir_and_file() {
    local dir_name=$1
    local file_name=$2
    
    mkdir -p "$dir_name"           # Create directory (ignore if it exists)
    touch "$dir_name/$file_name"   # Create an empty file
    echo "Created $dir_name/$file_name"
}

# Call the function
create_dir_and_file "test_dir" "sample.txt"
Expected Output:
A directory test_dir and a file sample.txt inside it will be created.

Troubleshooting:

If you get a permission error, use sudo or check your working directory permissions.
Step 2: Function with Return Values

Let’s modify the function to return a success/failure status.

create_dir_and_file() {
    local dir_name=$1
    local file_name=$2
    
    if mkdir -p "$dir_name" && touch "$dir_name/$file_name"; then
        echo "Success: Created $dir_name/$file_name"
        return 0  # Success
    else
        echo "Error: Failed to create $dir_name/$file_name"
        return 1  # Failure
    fi
}

# Call the function and check return value
if create_dir_and_file "test_dir" "sample.txt"; then
    echo "Operation succeeded!"
else
    echo "Operation failed!"
fi
Key Concept:

return 0 indicates success; return 1 indicates failure.
Task 2: Implement Error Handling

Step 1: Using trap for Cleanup

The trap command catches signals (e.g., script termination) to perform cleanup.

#!/bin/bash

cleanup() {
    echo "Cleaning up..."
    rm -rf test_dir  # Remove the directory on exit
}

trap cleanup EXIT  # Run cleanup when script exits

create_dir_and_file "test_dir" "sample.txt"
sleep 5  # Simulate script running
Expected Behavior:
The test_dir is deleted when the script exits (manually or due to an error).

Step 2: Exit on Error

Use exit to terminate the script if a critical error occurs.

#!/bin/bash

if ! mkdir "test_dir"; then
    echo "Critical: Failed to create directory"
    exit 1  # Exit script with error code
fi

echo "Directory created successfully"
Key Concept:

exit 1 stops the script immediately with an error status.
Task 3: Log Errors Based on Exit Status

Step 1: Logging Errors to a File

Create a script that logs errors to a file.

#!/bin/bash

LOG_FILE="error.log"

# Function to log errors
log_error() {
    local message=$1
    echo "$(date): ERROR - $message" >> "$LOG_FILE"
}

# Simulate a failing command
if ! grep "pattern" "nonexistent_file.txt" 2>/dev/null; then
    log_error "Failed to find 'pattern' in file"
fi
Expected Outcome:
An error.log file is created with a timestamped error message.

Step 2: Check Command Exit Status

Use $? to check the exit status of the last command.

#!/bin/bash

ls nonexistent_file.txt

if [ $? -ne 0 ]; then
    echo "Command failed with exit status $?"
fi
Key Concept:

$? holds the exit code of the last command (0 = success, non-zero = failure).
