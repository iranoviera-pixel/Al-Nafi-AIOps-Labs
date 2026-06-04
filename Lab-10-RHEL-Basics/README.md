Lab 10: Introduction to Scripting with Conditional Logic

Objectives

By the end of this lab, students will be able to:

Understand and implement basic conditional logic (if, else, elif) in Bash scripting.
Write scripts to check for file existence and system performance.
Interpret script outputs to make decisions based on conditions.
Apply troubleshooting techniques for common scripting errors.
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge (e.g., navigating directories, creating files).
Access to a Linux environment: Use the Al Nafi-provided cloud machine (click Start Lab to launch).
A text editor: nano or vim (run sudo apt install nano if not preinstalled).
Lab Setup

Launch the Cloud Machine:
Log in to your Al Nafi account and start the preconfigured Linux machine.
Open the terminal.
Create a Lab Directory:
mkdir scripting_lab && cd scripting_lab
Task 1: Check File Existence Using if Statements

Subtasks

Create a Test File:

touch sample.txt
Expected Outcome: A file named sample.txt is created in your directory.
Write the Script:
Use nano file_check.sh to create a script with the following code:

#!/bin/bash
if [ -f "sample.txt" ]; then
    echo "File exists!"
else
    echo "File not found."
fi
Key Concepts:
-f checks if a file exists.
if/else executes code based on the condition.
Run the Script:

chmod +x file_check.sh  # Make it executable
./file_check.sh
Expected Output: File exists!
Test with a Missing File:
Delete sample.txt (rm sample.txt) and rerun the script.

Expected Output: File not found.
Task 2: Check System Performance and Provide Recommendations

Subtasks

Write the Script:
Create performance_check.sh with:

#!/bin/bash
cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
mem_usage=$(free -m | awk '/Mem:/ {print $3/$2 * 100}')

if (( $(echo "$cpu_usage > 80" | bc -l) )); then
    echo "High CPU usage: $cpu_usage%. Consider closing heavy apps."
elif (( $(echo "$cpu_usage > 50" | bc -l) )); then
    echo "Moderate CPU usage: $cpu_usage%. Monitor for spikes."
else
    echo "CPU usage is normal: $cpu_usage%."
fi

if (( $(echo "$mem_usage > 80" | bc -l) )); then
    echo "High RAM usage: $mem_usage%. Check running processes."
else
    echo "RAM usage is normal: $mem_usage%."
fi
Key Concepts:
top and free extract CPU/RAM metrics.
elif adds multiple conditions.
Run the Script:

chmod +x performance_check.sh
./performance_check.sh
Expected Output: Recommendations based on your system’s current usage (e.g., "CPU usage is normal: 45%").
Task 3: Practice else and elif

Subtasks

Write a Number Classifier Script:
Create number_check.sh:

#!/bin/bash
read -p "Enter a number: " num

if [ $num -gt 0 ]; then
    echo "Positive number."
elif [ $num -lt 0 ]; then
    echo "Negative number."
else
    echo "Zero."
fi
Explanation:
read captures user input.
-gt (greater than) and -lt (less than) compare values.
Run the Script:

chmod +x number_check.sh
./number_check.sh
Test Cases:
Input 5 → Output: Positive number.
Input -3 → Output: Negative number.
Troubleshooting Tips

Permission Denied: Run chmod +x script_name.sh if you see this error.
Syntax Errors: Use bash -n script_name.sh to check for syntax issues.
Unexpected Output: Ensure variables are correctly referenced with $.
