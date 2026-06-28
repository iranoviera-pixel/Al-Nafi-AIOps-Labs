Lab 66: Automating System Configuration with Ansible

Objectives

By the end of this lab, students will be able to:

Write a basic Ansible playbook to automate software installation and configuration.
Use variables in playbooks to make them reusable across different systems.
Automate configuration tasks on multiple systems using Ansible inventory files.
Prerequisites

Before starting this lab, ensure you have:

Basic familiarity with Linux command line.
A Linux-based cloud machine provided by Al Nafi (click Start Lab to launch).
Ansible installed (will be covered in setup steps).
Lab Setup

Access Your Cloud Machine:

Log in to your Al Nafi account and click Start Lab to launch your pre-configured Linux machine.
Open the terminal once the machine is ready.
Install Ansible:
Run the following commands to install Ansible:

sudo apt update
sudo apt install ansible -y
Expected Outcome: Ansible is installed, and you can verify with ansible --version.
Create a Lab Directory:

mkdir ansible_lab && cd ansible_lab
Task 1: Write an Ansible Playbook for Software Installation

Subtask 1.1: Create a Basic Playbook

Create a file named install_apache.yml:

nano install_apache.yml
Add the following playbook content to install Apache: ```yaml

name: Install and start Apache hosts: localhost become: yes tasks:
name: Install Apache apt: name: apache2 state: present
name: Start Apache service service: name: apache2 state: started enabled: yes
- **Explanation**:  
  - `hosts: localhost`: Runs the playbook on the current machine.  
  - `become: yes`: Uses sudo for privileged tasks.  
  - `apt`: Installs Apache using the package manager.  
  - `service`: Ensures Apache is running and enabled on boot.
Save the file (Ctrl+O, Enter, Ctrl+X).

Subtask 1.2: Run the Playbook

Execute the playbook:
ansible-playbook install_apache.yml
Expected Outcome:
"PLAY RECAP" shows no failures.
Verify Apache is running: systemctl status apache2.
Task 2: Use Variables in Playbooks

Subtask 2.1: Create a Variable-Based Playbook

Create a new file install_web_server.yml:

nano install_web_server.yml
Add variables and tasks: ```yaml

name: Install and configure a web server hosts: localhost become: yes vars: web_server: apache2 # Default value tasks:
name: Install web server apt: name: "{{ web_server }}" state: present
name: Start web server service: name: "{{ web_server }}" state: started enabled: yes
- **Explanation**:  
  - `vars`: Defines `web_server` as a variable (default: `apache2`).  
  - Variables are referenced using `{{ }}`.
Subtask 2.2: Override Variables at Runtime

Run the playbook with Nginx instead:
ansible-playbook install_web_server.yml --extra-vars "web_server=nginx"
Expected Outcome: Nginx is installed and running. Verify with systemctl status nginx.
Task 3: Automate Configuration for Multiple Systems

Subtask 3.1: Create an Inventory File

Create inventory.ini:

nano inventory.ini
Add target systems (replace IP1, IP2 with dummy/test IPs or use localhost for this lab):

[web_servers]
server1 ansible_host=localhost
# server2 ansible_host=IP2
Subtask 3.2: Modify the Playbook for Multiple Hosts

Update install_web_server.yml to target the inventory group:

hosts: web_servers
Run the playbook:

ansible-playbook -i inventory.ini install_web_server.yml
Expected Outcome: The playbook executes on all hosts in web_servers.
Troubleshooting Tips

Permission Errors:

Ensure become: yes is included in the playbook.
Run with -K to prompt for a sudo password if needed:
ansible-playbook playbook.yml -K
Connection Issues:

Verify SSH access to remote hosts in the inventory.
Use ansible -i inventory.ini web_servers -m ping to test connectivity.
