Lab 69: Ansible Playbook Error Handling and Debugging

Objectives

By the end of this lab, you will be able to:

Use ignore_errors, failed_when, and block to handle errors in Ansible playbooks.
Debug Ansible playbooks using verbose mode (-v).
Write a basic script to automate debugging and fixing common Ansible issues.
Prerequisites

Before starting, ensure you have:

Basic knowledge of YAML syntax.
Familiarity with Ansible playbook structure.
Access to a Linux-based cloud machine (provided by Al Nafi—click Start Lab to begin).
Ansible installed (run ansible --version to verify).
Lab Setup

Click Start Lab to launch your cloud machine.
SSH into the machine using the provided credentials.
Verify Ansible is installed:
ansible --version
Expected Output: Displays Ansible version (e.g., 2.9.0 or higher).
Task 1: Implement Error Handling in Ansible

Subtask 1.1: Use ignore_errors

Objective: Continue playbook execution even if a task fails.

Create a playbook error_handling.yml: `yaml

hosts: localhost tasks:
name: This task will fail command: /bin/false ignore_errors: yes

name: This task will run even if the previous one fails debug: msg: "I ran despite the failure!"


Run the playbook:
ansible-playbook error_handling.yml
Expected Output: The first task fails (red), but the second task executes (green).
Subtask 1.2: Use failed_when

Objective: Define custom failure conditions.

Edit error_handling.yml:
- name: Check if a file exists (custom failure)
  command: ls /nonexistent_file
  register: result
  failed_when: "'No such file' not in result.stderr"
Run the playbook:
ansible-playbook error_handling.yml
Expected Output: Task fails only if No such file is not in the error message.
Subtask 1.3: Use block for Grouped Error Handling

Objective: Group tasks and handle errors collectively.

Update error_handling.yml:
- hosts: localhost
  tasks:
    - block:
        - name: Task 1 (may fail)
          command: /bin/false
        - name: Task 2
          debug:
            msg: "This won't run if Task 1 fails"
      rescue:
        - name: Rescue block
          debug:
            msg: "Caught an error!"
Run the playbook:
ansible-playbook error_handling.yml
Expected Output: The rescue blockexecutes if any task in theblock` fails.
Task 2: Debug with Verbose Mode (-v)

Objective: Use verbose output to troubleshoot playbooks.

Run any playbook with -v (verbose):
ansible-playbook -v error_handling.yml
Expected Output: Detailed logs showing task execution and variables.
Task 3: Write a Debugging Script

Objective: Automate common debugging steps.

Create debug_ansible.sh:
#!/bin/bash
echo "Debugging Ansible Playbook..."
playbook=$1

# Check syntax
ansible-playbook --syntax-check $playbook

# Run in verbose mode
ansible-playbook -v $playbook

# Check for common issues
grep -n "ignore_errors\|failed_when\|block" $playbook || echo "No error handlers found."
Make it executable:
chmod +x debug_ansible.sh
Run the script:
./debug_ansible.sh error_handling.yml
Expected Output: Syntax check, verbose execution, and error handler report.
