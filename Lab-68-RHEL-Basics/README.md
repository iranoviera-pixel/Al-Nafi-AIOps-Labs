Lab 68: Configuring SSH with Ansible

Objectives

By the end of this lab, you will be able to:

Configure SSH security settings using Ansible playbooks
Set up passwordless authentication between hosts using SSH keys
Automate SSH configuration for multiple servers
Understand basic Ansible playbook structure and modules
Prerequisites

Before starting this lab, you should have:

Basic Linux command-line knowledge
Familiarity with SSH concepts (client/server, key pairs)
Ansible installed (provided in Al Nafi cloud machines)
Access to at least two Linux servers (provided by Al Nafi cloud environment)
Note: Al Nafi provides pre-configured Linux machines. Click "Start Lab" to begin - no VM setup required.

Lab Setup

Launch your Al Nafi lab environment
Open a terminal window
Verify Ansible is installed by running:
ansible --version
You should see version 2.9 or higher
Task 1: Configure SSH Settings with Ansible

Step 1.1: Create Inventory File

Create a file named hosts in your home directory:

nano ~/hosts
Add the following content (replace IPs with your lab machines):

[webservers]
server1 ansible_host=192.168.1.10
server2 ansible_host=192.168.1.11

[all:vars]
ansible_user=ubuntu
ansible_ssh_private_key_file=~/.ssh/id_rsa
Step 1.2: Create SSH Configuration Playbook

Create configure_ssh.yml:

nano ~/configure_ssh.yml
Add this content: ```yaml

name: Configure Secure SSH Settings hosts: webservers become: yes tasks:

name: Disable root SSH login lineinfile: path: /etc/ssh/sshd_config regexp: '^PermitRootLogin' line: 'PermitRootLogin no' state: present notify: restart ssh

name: Disable password authentication lineinfile: path: /etc/ssh/sshd_config regexp: '^PasswordAuthentication' line: 'PasswordAuthentication no' state: present notify: restart ssh

handlers:

name: restart ssh service: name: sshd state: restarted

### **Step 1.3: Run the Playbook**
Execute the playbook:
```bash
ansible-playbook -i ~/hosts ~/configure_ssh.yml
Expected Output:

Playbook should complete with "PLAY RECAP" showing success for all tasks
SSH root login and password authentication will be disabled
Troubleshooting:

If connection fails, verify your inventory file IPs and SSH keys
Use -vvv flag for verbose output to debug connection issues
Task 2: Set Up Passwordless Authentication

Step 2.1: Generate SSH Key Pair

On your control node (main lab machine):

ssh-keygen -t rsa -b 4096 -N "" -f ~/.ssh/id_rsa
Step 2.2: Create Key Distribution Playbook

Create distribute_keys.yml: ```yaml

name: Distribute SSH Keys hosts: webservers tasks:
name: Copy public key to remote servers authorized_key: user: ubuntu state: present key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"

### **Step 2.3: Run Key Distribution**
```bash
ansible-playbook -i ~/hosts ~/distribute_keys.yml
Verification: Test passwordless login to any server:

ssh ubuntu@server1
You should login without being prompted for a password.

Task 3: Automate SSH Configuration for Multiple Hosts

Step 3.1: Create Combined Playbook

Create full_ssh_setup.yml combining both configurations: ```yaml

name: Complete SSH Setup hosts: webservers become: yes tasks:

name: Ensure SSH directory exists file: path: /home/ubuntu/.ssh state: directory mode: '0700' owner: ubuntu group: ubuntu

name: Copy public key authorized_key: user: ubuntu state: present key: "{{ lookup('file', '~/.ssh/id_rsa.pub') }}"

name: Harden SSH configuration block:

name: Disable root login lineinfile: path: /etc/ssh/sshd_config regexp: '^PermitRootLogin' line: 'PermitRootLogin no' state: present

name: Disable password auth lineinfile: path: /etc/ssh/sshd_config regexp: '^PasswordAuthentication' line: 'PasswordAuthentication no' state: present notify: restart ssh

handlers:

name: restart ssh service: name: sshd state: restarted

### **Step 3.2: Execute Full Automation**
```bash
ansible-playbook -i ~/hosts ~/full_ssh_setup.yml
