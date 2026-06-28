Lab 74: Rootless Containers in Podman

Objectives

By the end of this lab, students will be able to:

Understand the concept of rootless containers and their security benefits.
Configure Podman to run containers without root privileges.
Execute, manage, and automate rootless containers as a non-root user.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line.
A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Podman installed (included in Al Nafi lab environments).
Task 1: Set Up Podman for Rootless Execution

Why Rootless?

Rootless containers run without superuser privileges, reducing security risks. Podman natively supports this feature.

Steps:

Verify SubUID/SubGID Configuration
Rootless Podman requires subordinate user/group IDs. Check if they’re set:

grep $(whoami) /etc/subuid
grep $(whoami) /etc/subgid
Expected Output: Lines like youruser:100000:65536 (allocated IDs).
Troubleshooting: If empty, run sudo usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $(whoami) and reboot.
Test Rootless Podman
Run a simple container:

podman run hello-world
Expected Outcome: A "Hello from Docker" message (Podman uses Docker Hub by default).
Task 2: Run a Container as a Non-Root User

Steps:

Pull an Image
Download the Alpine Linux image:

podman pull alpine
Run a Container
Execute a shell inside the container:

podman run -it alpine sh
Verify Rootless: Run whoami inside the container. You’ll see root (container-internal), but the host process runs as your user.
Exit and List Containers
Type exit, then list containers:

podman ps -a
Task 3: Script to Manage Rootless Containers

Objective: Automate container lifecycle (create/start/stop) for a user.

Create a Script
Save as manage_containers.sh:

#!/bin/bash
CONTAINER_NAME="my_rootless_container"

case "$1" in
    create)
        podman run -d --name $CONTAINER_NAME alpine sleep infinity
        ;;
    start)
        podman start $CONTAINER_NAME
        ;;
    stop)
        podman stop $CONTAINER_NAME
        ;;
    *)
        echo "Usage: $0 {create|start|stop}"
        exit 1
esac
Make Script Executable

chmod +x manage_containers.sh
Test the Script

./manage_containers.sh create  # Creates container
./manage_containers.sh start   # Starts if stopped
podman ps                      # Verify running
