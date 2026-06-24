Lab 64: Writing Ansible Playbooks

Objectives

By the end of this lab, you will be able to:

Understand the basic structure of an Ansible playbook
Create a playbook to install packages on remote systems
Execute playbooks using ansible-playbook
Automate playbook creation with a simple script
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge
Ansible installed (Al Nafi cloud machines come pre-installed)
SSH access to at least two Linux target machines (inventory configured)
Sudo privileges on target machines
Lab Setup

Cloud Machines: Click "Start Lab" to launch your pre-configured Linux environment
Inventory File: /etc/ansible/hosts already contains sample groups
Validation: Run ansible --version to confirm Ansible is installed
Task 1: Write a Basic Package Installation Playbook

Step 1.1: Create Playbook Directory

mkdir ~/ansible-labs && cd ~/ansible-labs
Step 1.2: Create playbook.yml

---
- name: Install required packages
  hosts: webservers  # Group defined in /etc/ansible/hosts
  become: yes        # Use sudo
  
  tasks:
    - name: Install NGINX web server
      apt:
        name: nginx
        state: present
      when: ansible_os_family == "Debian"

    - name: Install Apache web server
      yum:
        name: httpd
        state: present
      when: ansible_os_family == "RedHat"
Key Concepts:

hosts: Target machine group
become: Privilege escalation
Conditional execution with when
Task 2: Execute the Playbook

Step 2.1: Verify Inventory

ansible webservers --list-hosts
Step 2.2: Run Playbook

ansible-playbook playbook.yml
Expected Output:

PLAY [Install required packages] ***************************************

TASK [Gathering Facts] ************************************************
ok: [server1]

TASK [Install NGINX web server] ***************************************
changed: [server1]

PLAY RECAP ************************************************************
server1  : ok=2  changed=1  unreachable=0  skipped=0  failed=0
Troubleshooting:

If connection fails: ansible webservers -m ping
Permission issues: Add -K to prompt for sudo password
Task 3: Automate Playbook Creation

Step 3.1: Create playbook_generator.sh

#!/bin/bash

read -p "Enter playbook name: " PB_NAME
read -p "Enter target group: " TARGET_GROUP
read -p "Package to install: " PACKAGE

cat > ${PB_NAME}.yml <<EOF
---
- name: Install $PACKAGE
  hosts: $TARGET_GROUP
  become: yes

  tasks:
    - name: Install $PACKAGE
      package:
        name: $PACKAGE
        state: present
EOF

echo "Playbook ${PB_NAME}.yml created!"
Step 3.2: Make Script Executable

chmod +x playbook_generator.sh
Step 3.3: Generate New Playbook

./playbook_generator.sh
# Follow prompts to create custom playbook
