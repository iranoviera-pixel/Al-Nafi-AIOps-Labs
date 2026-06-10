Lab 66: Understanding Web Servers

Objectives

By the end of this lab, you will be able to:

Understand the fundamental concepts of web servers and their role in serving web content.
Install and configure a basic Apache web server on a Linux machine.
Write and execute a script to manage the Apache service (start/stop).
Prerequisites

A Linux machine (Ubuntu/Debian recommended) with sudo privileges.
Basic familiarity with Linux command line.
Internet access for package installation.
Task 1: Research the Basics of Web Servers

Subtasks:

Understand what a web server is

A web server is software that delivers web content (HTML, CSS, JavaScript, etc.) to clients (browsers) over HTTP/HTTPS.
Popular open-source web servers: Apache, Nginx, Lighttpd.
Key components of a web server

HTTP Protocol: Handles client-server communication.
Virtual Hosting: Allows hosting multiple websites on a single server.
Configuration Files: Define server behavior (e.g., httpd.conf for Apache).
Expected Outcome

A clear understanding of how web servers function and their importance in web hosting.
Task 2: Install Apache Web Server on Linux

Subtasks:

Update the package repository
Run the following command to ensure your system is up-to-date:

sudo apt update && sudo apt upgrade -y
Install Apache
Use the following command to install Apache:

sudo apt install apache2 -y
Verify Apache installation
Check if Apache is running:

sudo systemctl status apache2
Expected Output: Active (running) status.
Test the default webpage
Open a browser and navigate to:

http://localhost
Expected Outcome: Apache default landing page ("It works!").
Troubleshooting Tips

If Apache fails to start, check logs:
sudo tail -f /var/log/apache2/error.log
Ensure port 80 is not blocked by a firewall.
Task 3: Write a Script to Start/Stop Apache

Subtasks:

Create a bash script
Open a text editor (e.g., nano) and create a script:

nano apache_manager.sh
Add the script logic
Paste the following code:

#!/bin/bash

# Function to display usage
usage() {
    echo "Usage: $0 {start|stop|restart|status}"
    exit 1
}

# Check if argument is provided
if [ "$#" -ne 1 ]; then
    usage
fi

case "$1" in
    start)
        sudo systemctl start apache2
        echo "Apache started successfully."
        ;;
    stop)
        sudo systemctl stop apache2
        echo "Apache stopped successfully."
        ;;
    restart)
        sudo systemctl restart apache2
        echo "Apache restarted successfully."
        ;;
    status)
        sudo systemctl status apache2
        ;;
    *)
        usage
        ;;
esac
Make the script executable
Run:

chmod +x apache_manager.sh
Test the script
Execute the script with different arguments:

./apache_manager.sh start
./apache_manager.sh status
./apache_manager.sh stop
Expected Outcome: Apache service responds to commands.
Troubleshooting Tips

If you get a "Permission denied" error, ensure the script is executable (chmod +x).
Use sudo if the script fails due to permission issues.
