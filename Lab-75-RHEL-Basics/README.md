Lab 75: Working with Container Registries

Objectives

By the end of this lab, you will be able to:

Pull container images from public registries like Docker Hub.
Push custom container images to a registry (Docker Hub or Quay.io).
Automate image management tasks using scripts.
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge (e.g., navigating directories, running commands).
Docker installed (Al Nafi’s cloud machines come pre-installed with Docker—just click Start Lab).
A Docker Hub or Quay.io account (free tier is sufficient).
Lab Setup

Cloud Machine: Click Start Lab to launch your Linux-based cloud machine (no VM setup required).
Verify Docker: Open the terminal and run:
docker --version
Expected output:
Docker version 20.10.12, build e91ed57
Task 1: Pull an Image from Docker Hub

Step 1: Search for an Image

Search for the official nginx image on Docker Hub:
docker search nginx
Expected output:
NAME      DESCRIPTION               STARS     OFFICIAL
nginx     Official build of Nginx.  18000     [OK]
Step 2: Pull the Image

Pull the nginx image:
docker pull nginx:latest
Expected output:
Status: Downloaded newer image for nginx:latest
Step 3: Verify the Image

List downloaded images:
docker images
Expected output:
REPOSITORY   TAG       IMAGE ID       CREATED       SIZE
nginx        latest    2b7d6430f78d   2 weeks ago   142MB
Troubleshooting:

If you see Error response from daemon, ensure Docker is running (sudo systemctl start docker).
Task 2: Push a Custom Image to a Registry

Step 1: Create a Custom Image

Create a simple Dockerfile:

echo "FROM alpine:latest" > Dockerfile
echo 'CMD echo "Hello from your custom image!"' >> Dockerfile
Build the image:

docker build -t my-custom-image .
Step 2: Tag the Image for Docker Hub

Log in to Docker Hub:

docker login
Enter your Docker Hub username and password when prompted.

Tag the image with your Docker Hub username:

docker tag my-custom-image <your-dockerhub-username>/my-custom-image:latest
Replace <your-dockerhub-username> with your actual username.

Step 3: Push the Image

Push to Docker Hub:
docker push <your-dockerhub-username>/my-custom-image:latest
Expected output:
latest: digest: sha256:... size: 528
Troubleshooting:

If you get denied: requested access to the resource is denied, ensure you’re logged in (docker login).
Task 3: Automate Image Management with a Script

Step 1: Create a Script

Write a script registry_manager.sh:
#!/bin/bash
# Pull an image
docker pull nginx:latest

# Push a custom image
docker push <your-dockerhub-username>/my-custom-image:latest
Step 2: Make the Script Executable

Set permissions:
chmod +x registry_manager.sh
Step 3: Run the Script

Execute the script:
./registry_manager.sh
Expected Outcome:
The script will pull nginx:latest and push your custom image without manual intervention.
