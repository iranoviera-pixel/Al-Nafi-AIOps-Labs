Lab 3: Using the vi Editor

Objectives

By the end of this lab, you will be able to:

Open, edit, and save files using the vi editor.
Use basic vi commands for navigation, insertion, deletion, and saving.
Automate file editing using a simple shell script.
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge (e.g., ls, cd, mkdir).
Access to a Linux-based system (Al Nafi’s cloud machine recommended).
No prior vi experience required—this lab is beginner-friendly!
Note: Al Nafi provides pre-configured Linux cloud machines. Click Start Lab to begin—no setup needed!

Task 1: Open and Edit a File Using vi

Step 1: Launch vi

Open the terminal.
Type the following command to create/open a file named practice.txt:
vi practice.txt
If the file doesn’t exist, vi will create it.
Expected Outcome: A blank file opens in vi (command mode).

Step 2: Enter Insert Mode

Press i to switch to insert mode (cursor starts blinking).
Type the following text:
Hello, this is my first vi file.  
I am learning basic vi editing.  
Expected Outcome: Text appears as you type.

Step 3: Save and Exit

Press Esc to return to command mode.
Type :wq and press Enter to save and exit.
Troubleshooting:

If you get stuck, press Esc + :q! to force-quit without saving.
Task 2: Basic vi Commands

Step 1: Reopen the File

vi practice.txt
Step 2: Practice Navigation (Command Mode)

Move cursor:
h (left), j (down), k (up), l (right).
0 (start of line), $ (end of line).
Step 3: Delete Text

Delete a character: Move cursor + press x.
Delete a line: Press dd.
Step 4: Undo/Redo

Undo: u
Redo: Ctrl + r
Step 5: Save Without Exiting

Press Esc + :w + Enter.
Key Concept: vi has two modes—command mode (navigation/commands) and insert mode (editing).

Task 3: Automate Editing with a Script

Step 1: Create a Script File

vi edit_script.sh
Step 2: Add Script Content

Press i and paste:

#!/bin/bash  
vi sample.txt <<EOF  
i  
This file was edited automatically.  
Press ESC and type :wq to save.  
EOF  
Step 3: Make the Script Executable

chmod +x edit_script.sh
Step 4: Run the Script

./edit_script.sh
Expected Outcome: sample.txt is created/edited automatically.
