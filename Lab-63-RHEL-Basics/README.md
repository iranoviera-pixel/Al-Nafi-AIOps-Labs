Lab 63: Introduction to YAML and Inventories

Objectives

By the end of this lab, you will be able to:

Understand YAML syntax and structure.
Create an Ansible inventory file in YAML format.
Write a basic script to generate dynamic inventories for Ansible playbooks.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line.
Access to a Linux-based cloud machine (provided by Al Nafi—click Start Lab to launch).
Ansible installed (pre-installed on Al Nafi machines; verify with ansible --version).
Task 1: Learn YAML Syntax and Structure

Step 1: Understand YAML Basics

YAML (YAML Ain’t Markup Language) is a human-readable data format used for configuration files. Key features:

Uses indentation (spaces, not tabs) to define hierarchy.
Key-value pairs are separated by :.
Lists are denoted with -.
Step 2: Create a Simple YAML File

Open a terminal and create a file named example.yml:
nano example.yml
Add the following content:
# Key-value pairs
name: "Lab 63"
author: "Student"
tools:
  - Ansible
  - YAML
  - Linux
# Nested structure
servers:
  web:
    ip: "192.168.1.10"
    os: "Ubuntu"
  db:
    ip: "192.168.1.20"
    os: "CentOS"
Save the file (Ctrl+O, Enter, Ctrl+X).
Expected Outcome:
You now have a valid YAML file with keys, values, lists, and nested structures.

Troubleshooting:

If you get errors, check for:
Consistent indentation (2 spaces per level).
No tabs (use spaces).
Task 2: Create an Ansible Inventory File in YAML

Step 1: Understand Ansible Inventories

An inventory file defines hosts and groups for Ansible to manage. YAML format is cleaner than INI.

Step 2: Write a YAML Inventory

Create inventory.yml:
nano inventory.yml
Add the following:
all:
  children:
    webservers:
      hosts:
        web1:
          ansible_host: "10.0.0.1"
          ansible_user: "ubuntu"
        web2:
          ansible_host: "10.0.0.2"
          ansible_user: "ubuntu"
    databases:
      hosts:
        db1:
          ansible_host: "10.0.0.3"
          ansible_user: "centos"
Save the file.
Expected Outcome:
Ansible can now target hosts like webservers or db1 in playbooks.

Verification:
Run ansible-inventory -i inventory.yml --list to confirm the structure.

Task 3: Write a Dynamic Inventory Script

Step 1: Understand Dynamic Inventories

Dynamic inventories generate host lists programmatically (e.g., from cloud APIs).

Step 2: Create a Basic Python Script

Create dynamic_inventory.py:
nano dynamic_inventory.py
Add this script (simulates fetching hosts from a cloud API):
#!/usr/bin/env python3
import json

inventory = {
    "webservers": {
        "hosts": ["web1", "web2"],
        "vars": {"ansible_user": "ubuntu"}
    },
    "dbservers": {
        "hosts": ["db1"],
        "vars": {"ansible_user": "centos"}
    }
}

print(json.dumps(inventory))
Make it executable:
chmod +x dynamic_inventory.py
Step 3: Test the Script

Run it directly:

./dynamic_inventory.py
Or with Ansible:

ansible -i dynamic_inventory.py webservers --list-hosts
Expected Outcome:
JSON output listing hosts in webservers and dbservers groups.

Troubleshooting:

Ensure Python 3 is installed (python3 --version).
If permissions are denied, re-run chmod +x.
