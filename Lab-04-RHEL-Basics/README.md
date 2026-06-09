Lab 4: Using the nano Editor

Objectives

By the end of this lab, students will be able to:

Open, create, and edit files using the nano text editor.
Save changes and exit files gracefully.
Automate text editing tasks using nano in combination with shell scripting.
Prerequisites

Before starting, ensure you have:

Basic familiarity with the Linux command line (e.g., navigating directories).
Access to a Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
No prior experience with nano is required.
Task 1: Open and Edit a File Using nano

Step 1: Launch nano

Open the terminal on your Linux machine.
Type the following command to open a new or existing file:
nano myfile.txt
If myfile.txt exists, it will open for editing. If not, nano creates it.
Step 2: Basic Editing

Use arrow keys to navigate.
Type or delete text as needed.
Example: Write a short line like:
Hello, this is my first nano file!
Expected Outcome

A file named myfile.txt is opened in the nano editor, and you can freely edit its content.
Troubleshooting

If you get a "Permission Denied" error, try:
sudo nano myfile.txt
(Note: Only use sudo if you have admin rights.)
Task 2: Save and Exit Files with nano

Step 1: Save Changes

Press Ctrl + O (Write Out).
Confirm the filename (myfile.txt) and press Enter.
Step 2: Exit nano

Press Ctrl + X to exit.
If you haven’t saved, nano will prompt you to save changes—press Y (Yes) or N (No).
Step 3: Verify the Saved File

In the terminal, type:
cat myfile.txt
This displays the file content. You should see the text you entered earlier.
Expected Outcome

The file is saved, and you exit nano without errors.
Task 3: Automate File Editing with nano

Step 1: Create a Script

Open a new file for the script:
nano edit_config.sh
Add the following code to append text to a config file:
#!/bin/bash
echo "Appending settings to config.txt..."
echo "auto_save=true" >> config.txt
echo "theme=dark" >> config.txt
Save (Ctrl + O) and exit (Ctrl + X).
Step 2: Make the Script Executable

Run:

chmod +x edit_config.sh
Step 3: Run the Script

./edit_config.sh
Step 4: Verify the Output

Check the contents of config.txt:

cat config.txt
You should see the appended lines:
auto_save=true
theme=dark
Expected Outcome

The script runs successfully, and the specified text is added to config.txt.
Troubleshooting

If the script doesn’t run, ensure:
It has execute permissions (chmod +x edit_config.sh).
You’re in the same directory as the script.
