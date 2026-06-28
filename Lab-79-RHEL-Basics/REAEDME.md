Lab 79: Podman Performance and Resource Management

Objectives

By the end of this lab, you will be able to:

Monitor container performance using top, ps, and podman stats.
Optimize CPU and memory allocation for containers.
Write a basic script to automate resource monitoring and adjustment.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line.
A running Linux-based cloud machine (provided by Al Nafi—click Start Lab to launch).
Podman installed (pre-installed on Al Nafi machines; verify with podman --version).
Task 1: Monitor Container Performance

Subtask 1.1: Use podman stats for Real-Time Monitoring

Start a sample container:
Run an Alpine Linux container in detached mode:

podman run -d --name demo_container alpine sleep 300
Expected Outcome: A container named demo_container will run in the background.

Monitor resource usage:
Open a new terminal and run:

podman stats
Expected Outcome: A live-updating table showing CPU, memory, and network usage for all running containers.
Troubleshooting: If no output appears, verify the container is running with podman ps.

Subtask 1.2: Use top and ps Inside a Container

Enter the container’s shell:

podman exec -it demo_container sh
Run top:
Inside the container, execute:

top
Expected Outcome: A process list showing CPU/memory usage (press q to exit).

Use ps for snapshot data:

ps aux
Expected Outcome: A static list of processes running in the container.

Task 2: Optimize Resource Allocation

Subtask 2.1: Set CPU Limits

Restart the container with CPU constraints:
Stop the existing container and run a new one with CPU limits:

podman run -d --name cpu_demo --cpus=0.5 alpine sleep 300
Explanation: Limits the container to 50% of a single CPU core.

Verify limits:

podman inspect cpu_demo | grep -i cpus
Expected Outcome: Output shows "NanoCPUs": 500000000 (0.5 CPU).

Subtask 2.2: Set Memory Limits

Run a container with memory constraints:

podman run -d --name mem_demo --memory=100m alpine sleep 300
Explanation: Limits the container to 100MB of RAM.

Verify memory limits:

podman inspect mem_demo | grep -i memory
Expected Outcome: Output shows "Memory": 104857600 (100MB in bytes).

Task 3: Automate Monitoring with a Script

Subtask 3.1: Write a Monitoring Script

Script to log resource usage:
Create monitor.sh using nano:

nano monitor.sh
Paste the following script:

#!/bin/bash
echo "Monitoring container resources..."
while true; do
    podman stats --no-stream >> container_stats.log
    sleep 5
done
Explanation: Logs stats every 5 seconds to container_stats.log.

Make the script executable:

chmod +x monitor.sh
Run the script:

./monitor.sh &
Expected Outcome: Background process logs stats. Press Enter to return to the shell.

Subtask 3.2: Adjust Resources Based on Usage

Script to adjust CPU if usage exceeds 80%:
Create adjust_cpu.sh:
#!/bin/bash
while true; do
    usage=$(podman stats --no-stream --format "{{.CPUPerc}}" demo_container | tr -d '%')
    if (( $(echo "$usage > 80" | bc -l) )); then
        podman update --cpus=1 demo_container
        echo "Increased CPU limit to 1 core at $(date)" >> adjustments.log
    fi
    sleep 10
done
Explanation: Checks CPU usage every 10 seconds and increases CPU limit if >80%.
