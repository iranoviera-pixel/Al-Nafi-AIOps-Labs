Lab 6: Introduction to Bash Scripting

Objectives

By the end of this lab, you will be able to:

Understand the basics of Bash scripting.
Write and execute simple Bash scripts.
Use variables and system commands in scripts.
Create interactive scripts that accept user input.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line (e.g., navigating directories, running commands).
Access to a Linux-based system (Al Nafi provides cloud machines—click Start Lab to begin).
A text editor (e.g., nano, vim, or gedit).
Task 1: Write a Simple "Hello World" Bash Script

Subtasks

Create a script file:

Open a terminal and run:
nano hello_world.sh
This opens the nano text editor to create a new file named hello_world.sh.
Write the script:

Add the following code to the file:
#!/bin/bash
echo "Hello World!"
#!/bin/bash (shebang) tells the system this is a Bash script.
echo prints the text to the terminal.
Save and exit:

Press Ctrl+O to save, then Enter.
Press Ctrl+X to exit nano.
Make the script executable:

Run:
chmod +x hello_world.sh
chmod +x gives the file execute permissions.
Run the script:

Execute it with:
./hello_world.sh
Expected Output:
Hello World!
Troubleshooting

If you see Permission denied, ensure you ran chmod +x.
If the script doesn’t run, check the shebang line is correct.
Task 2: Create an Interactive Script (User Greeting)

Subtasks

Create a new script:

Run:
nano greet_user.sh
Write the script:

Add this code:
#!/bin/bash
echo "What is your name?"
read name
echo "Hello, $name! Welcome to Bash scripting."
read captures user input and stores it in the variable name.
$name references the variable’s value.
Save, make executable, and run:

Repeat Task 1 steps 3–5 for greet_user.sh.
Run:
./greet_user.sh
Example Output:
What is your name?
[User enters: Alice]
Hello, Alice! Welcome to Bash scripting.
Key Concept

Variables (name`) store data for later use in scripts.
Task 3: Check Disk Usage

Subtasks

Create the script:

Run:
nano disk_check.sh
Write the script:

Add this code:
#!/bin/bash
echo "Disk Usage Report:"
df -h
df -h shows disk usage in human-readable format (e.g., GB, KB).
Save, make executable, and run:

Repeat Task 1 steps 3–5 for disk_check.sh.
Run:
./disk_check.sh
Expected Output:
Disk Usage Report:
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1        20G  5.2G   14G  28% /
Troubleshooting

If df -h fails, ensure you have proper permissions (run with sudo if needed).
