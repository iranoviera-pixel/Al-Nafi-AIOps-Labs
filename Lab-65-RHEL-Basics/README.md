Lab 65: Using Ansible Roles

Objectives

By the end of this lab, you will be able to:

Understand the structure and benefits of Ansible roles.
Create a custom Ansible role to configure Apache web server.
Use a playbook to apply the role across multiple hosts.
Automate role deployment using a simple shell script.
Prerequisites

Before starting, ensure you have:

Basic knowledge of Linux command line and YAML syntax.
Ansible installed (version 2.9 or later).
Access to at least two Linux-based cloud machines (provided by Al Nafi—click Start Lab to launch them).
SSH access to the machines with sudo privileges.
Task 1: Create an Ansible Role for Apache

Step 1: Set Up the Role Directory Structure

On your control node (primary cloud machine), run:
mkdir -p roles/apache/{tasks,handlers,templates,files,vars,defaults,meta}
This creates the standard Ansible role directory structure.
Step 2: Define the Apache Installation Task

Create the main tasks file:
nano roles/apache/tasks/main.yml
Add the following YAML to install and start Apache: `yaml

name: Install Apache apt: name: apache2 state: present when: ansible_os_family == 'Debian'

name: Start and enable Apache service: name: apache2 state: started enabled: yes


Step 3: Add a Custom Index Page (Optional)

Create a template for index.html:
nano roles/apache/templates/index.html.j2
Add basic HTML:
<html>
  <body>
    <h1>Welcome to {{ ansible_hostname }}!</h1>
  </body>
</html>
Add a task to deploy the template in roles/apache/tasks/main.yml:
- name: Deploy index.html
  template:
    src: index.html.j2
    dest: /var/www/html/index.html
Expected Outcome:
The role directory is created with tasks to install Apache and deploy a custom webpage.

Task 2: Write a Playbook to Use the Role

Step 1: Create the Playbook

Create a file named apache_deploy.yml:
nano apache_deploy.yml
Add the following content: `yaml

hosts: webservers become: yes roles:
apache

Step 2: Define Inventory

Create/edit /etc/ansible/hosts and add your target machines under [webservers]:
[webservers]
server1 ansible_host=<IP_ADDRESS_1>
server2 ansible_host=<IP_ADDRESS_2>
Step 3: Run the Playbook

the playbook:
ansible-playbook apache_deploy.yml
Expected Outcome:
Apache is installed and running on all hosts in the webservers group. Verify by visiting http://<IP_ADDRESS> in a browser.

Task 3: Automate Role Deployment with a Script

Step 1: Create a Deployment Script

Write a shell script named deploy_roles.sh:
nano deploy_roles.sh
Add the following:
#!/bin/bash
# Deploy Apache role using Ansible
ansible-playbook apache_deploy.yml
echo "Apache deployment complete!"
Step 2: Make the Script Executable

chmod +x deploy_roles.sh
Step 3: Run the Script

./deploy_roles.sh
Expected Outcome:
The script executes the playbook, deploying Apache automatically.
