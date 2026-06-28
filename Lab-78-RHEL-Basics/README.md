Lab 78: Networking Containers in Podman

Objectives

By the end of this lab, you will be able to:

Forward container ports to the host system for external access
Create and manage a Podman network bridge for inter-container communication
Automate container networking configurations using scripts
Prerequisites

Before starting, ensure you have:

Basic Linux command-line knowledge
Podman installed (Al Nafi cloud machines come pre-installed)
A running Linux system (use Al Nafi's cloud machine by clicking "Start Lab")
Task 1: Run a Container with Port Forwarding

Objective: Expose a containerized web server to your host system

Step 1.1: Launch a Web Server Container

podman run -d --name web_server -p 8080:80 docker.io/library/nginx
Explanation:

-d: Runs container in detached mode
--name web_server: Names the container
-p 8080:80: Maps host port 8080 to container port 80
docker.io/library/nginx: Official Nginx image
Expected Output: A container ID confirming successful launch

Step 1.2: Verify Port Forwarding

curl http://localhost:8080
Expected Output: The default Nginx welcome page HTML

Troubleshooting:

If connection fails, check container status with podman ps -a
Ensure no other service is using port 8080 (ss -tulnp | grep 8080)
Task 2: Set Up a Podman Network Bridge

Objective: Create a private network for container communication

Step 2.1: Create a Bridge Network

podman network create lab_network
Explanation: Creates a new bridge network named "lab_network"

Step 2.2: Launch Containers on the Network

podman run -d --name container1 --network lab_network alpine sleep infinity
podman run -d --name container2 --network lab_network alpine sleep infinity
Step 2.3: Test Connectivity

podman exec -it container1 ping -c 3 container2
Expected Output: Successful ping responses showing containers can communicate

Key Concept: Bridge networks enable DNS resolution between containers by name

Task 3: Automate Networking with Scripts

Objective: Create a script to deploy pre-configured containers

Step 3.1: Create Network Configuration Script

cat > network_setup.sh << 'EOF'
#!/bin/bash

# Create network if not exists
podman network exists lab_network || podman network create lab_network

# Launch containers
podman run -d --name web_app -p 8080:80 --network lab_network docker.io/library/nginx
podman run -d --name database --network lab_network docker.io/library/redis

echo "Network setup complete. Access web app at localhost:8080"
EOF
Step 3.2: Make Script Executable

chmod +x network_setup.sh
Step 3.3: Run the Script

./network_setup.sh
Verification:

podman ps
curl http://localhost:8080
Expected Outcome:

Two running containers (nginx and redis)
Accessible web server on port 8080
