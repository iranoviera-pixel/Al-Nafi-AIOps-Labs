Prerequisites

A Linux system (Ubuntu 20.04+ or CentOS 7+ recommended)
Basic command line familiarity
sudo privileges for process management tasks
htop installed (run sudo apt install htop or sudo yum install htop)
Task 1: Viewing Running Processes

Subtask 1.1: Using ps command

Step 1: View all running processes for current user

ps -u $USER
Expected Output:

  PID TTY          TIME CMD
 1234 pts/0    00:00:00 bash
 5678 pts/0    00:00:01 python
Step 2: View all system processes in full format

ps aux
Key Concepts:

a = show processes for all users
u = display user-oriented format
x = include processes without a TTY
Subtask 1.2: Using top command

Step 1: Launch the process monitor

top
Key Features to Note:

System uptime and load averages
CPU and memory usage statistics
Process list sorted by CPU usage (press M to sort by memory)
Step 2: Exit top by pressing q

Subtask 1.3: Using htop (interactive process viewer)

Step 1: Launch htop

htop
Key Operations:

F6 to sort by different columns
F9 to send signals to processes
F10 to exit
Troubleshooting Tip: If htop isn't installed:

sudo apt update && sudo apt install htop  # Debian/Ubuntu
sudo yum install htop                     # CentOS/RHEL
Task 2: Finding and Killing Processes by Name

Subtask 2.1: Finding Processes

Step 1: Find all processes containing "python"

pgrep -l python
Alternative Method:

ps aux | grep python
Subtask 2.2: Killing Processes

Step 1: Gracefully terminate a process by name)

pkill python
Step 2: Forcefully kill a process (if unresponsive)

pkill -9 python
Subtask 2.3: Create a Kill Script

Step 1: Create process_killer.sh

#!/bin/bash

if [ -z "$1" ]; then
    echo "Usage: $0 <process_name>"
    exit 1
fi

echo "Searching for processes containing: $1"
pgrep -l "$1"

read -p "Kill these processes? (y/n) " answer

if [ "$answer" = "y" ]; then
    pkill "$1"
    echo "Processes terminated."
else
    echo "Operation cancelled."
fi
Step 2: Make it executable and run

chmod +x process_killer.sh
./process_killer.sh python
Task 3: Process Priority Management

Subtask 3.1: Launching Processes with nice

Step 1: Start a process with low priority

nice -n 19 python3 long_running_script.py
Key Concept: Nice values range from -20 (highest priority) to 19 (lowest)

Subtask 3.2: Adjusting Priority with renice

Step 1: Find a process to reprioritize

pgrep python
Step 2: Change priority (example PID 1234)

sudo renice -n 10 -p 1234
Subtask 3.3: Priority Management Script

Step 1: Create priority_manager.sh

#!/bin/bash

echo "Current process priorities:"
ps -eo pid,ni,cmd | head -n 5

read -p "Enter PID to renice: " pid
read -p "Enter new nice value (-20 to 19): " niceval

if ! sudo renice -n $niceval -p $pid; then
    echo "Failed to change priority. Try with sudo?"
fi
    echo "Priority changed successfully for PID $pid"
fi

