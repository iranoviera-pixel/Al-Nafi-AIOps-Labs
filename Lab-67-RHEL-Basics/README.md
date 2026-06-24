Lab 67: Managing Users and Groups with Ansible

Objectives

By the end of this lab, students will be able to:

Understand Ansible's user and group modules for system administration.
Create and manage users and groups across multiple Linux systems using Ansible.
Write and execute an Ansible playbook for automated user/group management.
Apply best practices for secure user management (e.g., SSH key authentication).
Prerequisites

Before starting, ensure you have:

Basic Linux CLI knowledge (e.g., navigating directories, running commands).
Ansible installed (Al Nafi cloud machines come pre-installed with Ansible).
SSH access to target systems (for multi-machine tasks; the lab uses localhost by default).
YAML syntax familiarity (indentation matters!).
Lab Setup

Cloud Machines: Click Start Lab in your Al Nafi dashboard to launch a pre-configured Linux machine with Ansible.
Inventory File: Ansible uses /etc/ansible/hosts by default. For this lab, we’ll use localhost.
Task 1: Create Users and Groups with Ansible

Subtask 1.1: Write a Playbook to Create a Group

Open a terminal and create a new playbook file:

nano create_users_groups.yml
Add the following YAML code to create a group named developers: `yaml

name: Manage users and groups hosts: localhost become: true # Run as root tasks:
name: Ensure group 'developers' exists ansible.builtin.group: name: developers state: present
- **Explanation**:  
  - `become: true`: Escalates privileges to root (required for user/group management).  
  - `state: present`: Ensures the group exists (use `absent` to remove).  
Save the file (Ctrl+O, then Ctrl+X).

Subtask 1.2: Run the Playbook

Execute the playbook:
ansible-playbook create_users_groups.yml
Expected Output:
PLAY [Manage users and groups] *******************************************
TASK [Ensure group 'developers' exists] **********************************
changed: [localhost]
PLAY RECAP ***************************************************************
localhost: ok=1 changed=1 unreachable=0 failed=0
Verify the group was created:
grep developers /etc/group
Troubleshooting: If the playbook fails, check YAML indentation and run ansible-playbook --syntax-check create_users_groups.yml.
Task 2: Add Users with Ansible

Subtask 2.1: Add a User to the Group

Edit create_users_groups.yml and append this task:

    - name: Add user 'jdoe' to 'developers'
      ansible.builtin.user:
        name: jdoe
        group: developers
        shell: /bin/bash
        password: "{{ 'Password123' | password_hash('sha512') }}"
        state: present
Key Concepts:
password: Hashed for security (never store plaintext passwords!).
shell: Sets the default shell for the user.
Re-run the playbook:

ansible-playbook create_users_groups.yml
Verify the user:

id jdoe
Expected Output:
uid=1001(jdoe) gid=1001(developers) groups=1001(developers)
Task 3: Automate Across Multiple Systems

Subtask 3.1: Modify Inventory for Remote Hosts

Edit /etc/ansible/hosts and add target IPs under a group [webservers]:
[webservers]
192.168.1.10
192.168.1.11
Subtask 3.2: Update the Playbook

Change hosts: localhost to hosts: webservers in create_users_groups.yml.

Run the playbook:

ansible-playbook -k create_users_groups.yml  # -k prompts for SSH password
Note: Use SSH keys (ansible-playbook -i inventory.ini playbook.yml) for production.
