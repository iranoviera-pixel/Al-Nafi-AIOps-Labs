Lab 76: Using Systemd to Manage Containers

Objectives

By the end of this lab, you will be able to:

Understand how systemd can manage containerized applications.
Create and configure a systemd service unit for a container.
Start, stop, and monitor containers using systemd commands.
Automate the creation of systemd unit files for containers using a script.
Prerequisites

Before starting, ensure you have:

A Linux-based machine (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with Linux command line and systemd.
Docker or Podman installed (Docker is used in this lab, but Podman commands are similar).
Root or sudo privileges to manage systemd services.
Task 1: Create a Systemd Service Unit for a Container

Step 1: Pull a Sample Container Image

Run the following command to download a lightweight container image (e.g., Nginx):

docker pull nginx:alpine
Expected Outcome: The Nginx Alpine image is downloaded to your machine.

Step 2: Create a Systemd Service Unit File

Open a new systemd unit file using a text editor:

sudo nano /etc/systemd/system/nginx-container.service
Add the following content to the service file:

[Unit]
Description=Nginx Container
After=docker.service
[Service]
Restart=always
ExecStart=/usr/bin/docker run --name nginx-lab -p 8080:80 nginx:alpine
ExecStop=/usr/bin/docker stop nginx-lab
ExecStopPost=/usr/bin/docker rm nginx-lab

[Install]
WantedBy=multi-user.target
Explanation:

After=docker.service: Ensures Docker is running before starting the container.
ExecStart: Command to start the container.
ExecStop and ExecStopPost: Commands to stop and remove the container.
Save the file (Ctrl+O, then Ctrl+X in nano).

Step 3: Reload Systemd and Start the Service

Reload systemd to recognize the new service:
sudo systemctl daemon-reload
Start the service:
sudo systemctl start nginx-container
Verify the container is running:
docker ps
Expected Outcome: The Nginx` container appears in the list of running containers.
Task 2: Start, Stop, and Monitor the Container

Step 1: Check Service Status

Run:

sudo systemctl status nginx-container
Expected Outcome: The output shows the service as "running."

Step 2: Stop the Container

Stop the service:
sudo systemctl stop nginx-container
Verify the container is stopped:
docker ps -a
Expected Outcome: The container is no longer running but may appear as "Exited."
Step 3: Enable Automatic Startup

To start the container on boot:

sudo systemctl enable nginx-container
Expected Outcome: The service is enabled for startup at boot.

Task 3: Automate Systemd Unit File Creation

Step 1: Create a Bash Script

Open a new script file:
nano create-container-service.sh
Add the following script:
#!/bin/bash
# Usage: ./create-container-service.sh <container-name> <image-name> <host-port> <container-port>

if [ $# -ne 4 ]; then
    echo "Usage: $0 <container-name> <image-name> <host-port> <container-port>"
    exit 1
fi

SERVICE_FILE="/etc/systemd/system/${1}.service"

cat <<EOF | sudo tee $SERVICE_FILE > /dev/null
[Unit]
Description=$1} Container
After=docker.service

[Service]
Restart=always
ExecStart=/usr/bin/docker run --name $1 -p $3:$4 $2
ExecStop=/usr/bin/docker stop $1
ExecStopPost=/usr/bin/docker rm $1

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
echo "Systemd service $1 created and reloaded."
Make the script executable:
chmod +x create-container-service.sh
Step 2: Run the Script

Execute the script to create a new service (e.g., for a Redis container):

sudo ./create-container-service.sh redis-container redis 6379 6379
Expected Outcome: A new systemd unit file redis-container.service is created and loaded.

