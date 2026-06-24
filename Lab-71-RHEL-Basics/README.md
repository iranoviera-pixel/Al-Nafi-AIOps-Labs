Lab 71: Podman vs. Docker

Objectives

By the end of this lab, students will be able to:

Install and configure Podman on a CentOS system.
Create, manage, and run containers using Podman.
Compare Podman and Docker commands to understand their differences.
Write a basic script to automate container creation.
Prerequisites

Before starting this lab, ensure you have:

A CentOS 7/8/9 system (provided by Al Nafi's cloud machines—click Start Lab to launch your pre-configured environment).
Basic familiarity with Linux command-line operations.
Sudo or root privileges (provided in Al Nafi's environment).
Task 1: Install Podman on CentOS

Step 1: Update System Packages

Open a terminal and run:

sudo yum update -y
Expected Outcome: All system packages are updated.

Step 2: Install Podman

Install Podman using the default CentOS repositories:

sudo yum install -y podman
Expected Outcome: Podman is installed. Verify with:

podman --version
Troubleshooting: If the command fails, enable the extras repository:

sudo yum-config-manager --enable extras
Task 2: Create and Run a Container with Podman

Step 1: Pull a Container Image

Pull the official Alpine Linux image:

podman pull alpine
Expected Outcome: Image is downloaded. Verify with:

podman images
Step 2: Run the Container

Start an interactive Alpine container:

podman run -it --name my_alpine alpine sh
Key Concept:

-it: Allocates a terminal for interaction.
--name: Assigns a name to the container.
Expected Outcome: You’re inside the container shell. Exit with exit.

Step 3: List Running/Stopped Containers

podman ps -a
Compare to Docker:

Docker: docker ps -a
Podman: No daemon required (unlike Docker).
Task 3: Compare Podman and Docker Commands

Key Differences Table

Action	Docker Command	Podman Command
List images	docker images	podman images
Run container	docker run	podman run
Remove image	docker rmi <image>	podman rmi <image>
Daemon status	systemctl status docker	Not applicable (daemonless)
Hands-On Comparison:

Try running an Nginx container with both tools:
# Podman
podman run -d --name nginx_podman -p 8080:80 nginx

# Docker (if installed)
docker run -d --name nginx_docker -p 8090:80 nginx
Access both services via curl localhost:8080 and curl localhost:8090.
Task 4: Automate Container Creation with a Script

Step 1: Write a Bash Script

Create create_container.sh:

#!/bin/bash
# This script creates an Nginx container with Podman
podman run -d --name auto_nginx -p 8081:80 nginx
echo "Nginx container is running on port 8081!"
Step 2: Make the Script Executable

chmod +x create_container.sh
Step 3: Run the Script

./create_container.sh
Expected Outcome: Nginx container starts automatically. Verify with:

curl localhost:8081
