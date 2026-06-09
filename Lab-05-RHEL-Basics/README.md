Lab 5: Environment Variables and Aliases

Objectives

By the end of this lab, you will be able to:

Understand what environment variables are and how to view them.
Create and modify environment variables in a Linux environment.
Use aliases to simplify frequently used commands.
Automate the setup of environment variables and aliases using scripts.
Prerequisites

Before starting, ensure you have:

Basic familiarity with the Linux command line.
Access to a Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
A text editor like nano or vim installed (usually available by default in Linux).
Task 1: Display Environment Variables Using printenv

Step 1: Open the Terminal

Launch the terminal in your Linux environment.
Step 2: List All Environment Variables

Run the following command to display all environment variables:

printenv
Expected Output:
A list of variables like PATH, USER, HOME, etc., with their assigned values.

Step 3: Display a Specific Variable

To view the value of a specific variable (e.g., USER), use:

printenv USER
Expected Output:
Your username (e.g., student).

Troubleshooting Tip:
If the variable doesn’t exist, the command will return nothing. Ensure you’ve spelled the variable name correctly.

Task 2: Set a New Environment Variable

Step 1: Create a Temporary Variable

Set a variable for the current session:

export MY_VAR="Hello, Lab 5!"
Verify it exists:

printenv MY_VAR
Expected Output:
Hello, Lab 5!

Step 2: Make the Variable Persistent

To retain the variable after reboot, add it to ~/.bashrc:

Open the file:
nano ~/.bashrc
Add this line at the end:
export MY_VAR="Hello, Lab 5!"
Save (Ctrl+O), exit (Ctrl+X), and reload:
source ~/.bashrc
Troubleshooting Tip:
If the variable doesn’t appear, ensure you’ve run source ~/.bashrc or reopened the terminal.

Task 3: Create an Alias for Commonly Used Commands

Step 1: Define a Temporary Alias

Create an alias to shorten ls -la:

alias ll='ls -la'
Test it:

ll
Expected Output:
A detailed list of files/directories (like ls -la).

Step 2: Make the Alias Permanent

Edit ~/.bashrc:
nano ~/.bashrc
Add:
alias ll='ls -la'
Save, exit, and reload:
source ~/.bashrc
Troubleshooting Tip:
If the alias doesn’t work, check for typos and ensure ~/.bashrc is loaded.

Task 4: Automate Setup with a Script

Step 1: Create a Script File

Open a new file:
nano setup_env.sh
Add the following:
#!/bin/bash
# Add environment variables
echo 'export MY_VAR="Hello, Lab 5!"' >> ~/.bashrc
# Add aliases
echo 'alias ll="ls -la"' >> ~/.bashrc
# Reload configuration
source ~/.bashrc
echo "Setup complete!"
Step 2: Make the Script Executable

chmod +x setup_env.sh
Step 3: Run the Script

./setup_env.sh
Expected Output:
Setup complete! and the variable/alias will now persist.

Troubleshooting Tip:
If you get a "Permission denied" error, ensure you ran chmod +x.
