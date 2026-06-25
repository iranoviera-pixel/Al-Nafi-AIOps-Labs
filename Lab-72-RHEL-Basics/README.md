Lab 72: Building Container Images with Podman

Objectives

By the end of this lab, students will be able to:

Understand the basics of containerization and Podman.
Create a Dockerfile for a simple Python application.
Build a container image using podman build.
Automate image building and tagging with a shell script.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line.
A Linux-based machine (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Podman installed (pre-installed on Al Nafi machines; verify with podman --version).
A text editor (e.g., nano, vim, or gedit).
Task 1: Create a Dockerfile for a Python Application

Subtasks

1.1 Set Up a Project Directory

Open the terminal.
Run the following commands to create a project folder and navigate into it:
mkdir python-app && cd python-app
1.2 Create a Simple Python Script

Create a file named app.py using a text editor:
nano app.py
Add the following Python code to print a welcome message:
# app.py
print("Welcome to the Podman Lab!")
Save and exit (Ctrl+O, Enter, Ctrl+X in nano).
1.3 Create the Dockerfile

Create a file named Dockerfile in the same directory:
nano Dockerfile
Add the following content to the Dockerfile:
# Use the official Python base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the Python script into the container
COPY app.py .

# Run the script when the container starts
CMD ["python", "app.py"]
Save and exit.
Task 2: Build the Image Using Podman

Subtasks

2.1 Build the Container Image

Run the following command to build the image:
podman build -t python-app .
-t python-app: Tags the image with the name python-app.
.: Specifies the build context (current directory).
2.2 Verify the Image

List all images to confirm the build was successful:
podman images
Expected output: A list of images including python-app.
2.3 Run the Container

Execute the container to test it:
podman run python-app
Expected output: Welcome to the Podman Lab!
Task 3: Automate Building and Tagging with a Script

Subtasks

3.1 Create a Build Script

Create a file named build.sh:
nano build.sh
Add the following script to automate building and tagging:
#!/bin/bash

# Define variables
IMAGE_NAME="python-app"
TAG="v1.0"

# Build the image
podman build -t $IMAGE_NAME:$TAG .

# Verify the image
podman images | grep $IMAGE_NAME
Save and exit.
3.2 Make the Script Executable

Run:
chmod +x build.sh
3.3 Execute the Script

Run the script:
./build.sh
Expected output: The image is built and listed with the tag v1.0.
