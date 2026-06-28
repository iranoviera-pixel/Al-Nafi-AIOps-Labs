Lab 77: Automating Container Setup with Podman

Objectives

By the end of this lab, you will be able to:

Write a Bash script to automate Podman container operations (create, run, stop).
Integrate the script with systemd for automatic container startup at boot.
Verify the automation by testing container behavior during system startup.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line.
A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Podman installed (included in most modern Linux distributions; we'll verify installation in the lab).
Task 1: Write a Podman Automation Script

Step 1: Verify Podman Installation

Run the following command to check if Podman is installed:

podman --version
Expected Output:
podman version 4.x.x (or similar).
If not installed, run:

sudo apt-get install podman -y  # Debian/Ubuntu
sudo dnf install podman -y      # Fedora/CentOS
Step 2: Create a Bash Script

Create a script named container_manager.sh to automate container operations:

#!/bin/bash

# Define container name and image
CONTAINER_NAME="demo-container"
IMAGE="docker.io/library/nginx:latest"

# Function to start the container
start_container() {
    podman run -d --name $CONTAINER_NAME -p 8080:80 $IMAGE
    echo "Container $CONTAINER_NAME started."
}

# Function to stop the container
stop_container() {
    podman stop $CONTAINER_NAME
    podman rm $CONTAINER_NAME
    echo "Container $CONTAINER_NAME stopped and removed."
}

# Main logic
case "$1" in
    start)
        start_container
        ;;
    stop)
        stop_container
        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
esac
Key Concepts:

podman run: Creates and starts a container.
-d: Runs in detached mode.
-p 8080:80: Maps host port 8080 to container port 80.
Step 3: Make the Script Executable

chmod +x container_manager.sh
Step 4: Test the Script

Start the container:

./container_manager.sh start
Verify:

podman ps
Should show the running demo-container.

Stop the container:

./container_manager.sh stop
Task 2: Integrate with systemd for Auto-Start

Step 1: Create a systemd Service File

Create /etc/systemd/system/container-demo.service:

[Unit]
Description=Podman Container Demo
After=network.target

[Service]
Type=oneshot
ExecStart=/path/to/container_manager.sh start
ExecStop=/path/to/container_manager.sh stop
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
Replace /path/to/ with the actual path to your script (e.g., /home/user/).

Step 2: Reload systemd and Enable the Service

sudo systemctl daemon-reload
sudo systemctl enable container-demo
Step 3: Test Auto-Start

Reboot your machine or simulate with:
sudo systemctl start container-demo
Verify the container is running:
podman ps
Troubleshooting:
If the container fails to start, check logs:

journalctl -u container-demo -b
Task 3: Validate Container Auto-Start at Boot

Step 1: Reboot the System

sudo reboot
Step 2: Verify Post-Reboot

After logging back in, run:

podman ps
Expected Outcome:
The demo-container should be listed as running.
