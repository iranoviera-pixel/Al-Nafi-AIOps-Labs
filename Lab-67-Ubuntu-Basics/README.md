Lab 67: Setting Up a Basic Apache Server

Objectives

By the end of this lab, you will be able to:

Install and configure Apache HTTP Server on a Linux system.
Create and serve a basic HTML page using Apache.
Write and execute a deployment script to automate website testing.
Verify Apache server functionality through local access.
Prerequisites

A Linux system (Ubuntu/Debian/CentOS)
Terminal access with sudo privileges
Basic knowledge of Linux commands
Text editor (nano/vim/gedit)
Task 1: Install and Configure Apache on Linux

Step 1.1: Update System Packages

sudo apt update && sudo apt upgrade -y
Expected Outcome: System packages are updated to their latest versions.

Step 1.2: Install Apache

For Ubuntu/Debian:

sudo apt install apache2 -y
For CentOS/RHEL:

sudo yum install httpd -y
Expected Outcome: Apache is installed without errors.

Step 1.3: Start and Enable Apache

sudo systemctl start apache2  # Ubuntu/Debian
sudo systemctl enable apache2
For CentOS:

sudo systemctl start httpd
sudo systemctl enable httpd
Verification:

sudo systemctl status apache2  # Should show "active (running)"
Troubleshooting Tip: If you get a firewall error, allow Apache traffic:

sudo ufw allow 'Apache'  # Ubuntu/Debian
sudo firewall-cmd --permanent --add-service=http --zone=public  # CentOS
Task 2: Create and Configure a Basic HTML Page

Step 2.1: Navigate to Apache Web Directory

cd /var/www/html
Step 2.2: Create a Sample HTML Page

sudo nano index.html
Paste the following code:

<!DOCTYPE html>
<html>
<head>
    <title>Apache Test Page</title>
</head>
<body>
    <h1>Hello, Apache Server!</h1>
    <p>This is a test page served by Apache.</p>
</body>
</html>
Save and exit (Ctrl+O, Enter, Ctrl+X).

Expected Outcome: A basic index.html file is created in /var/www/html.

Step 2.3: Set Proper Permissions

sudo chown -R $USER:$USER /var/www/html
sudo chmod -R 755 /var/www/html
Task 3: Deploy and Test the Website

Step 3.1: Write a Deployment Script

Create a script to automate testing:

nano deploy_test.sh
Paste the following:

#!/bin/bash
echo "Deploying test page..."
sudo cp index.html /var/www/html/
echo "Restarting Apache..."
sudo systemctl restart apache2
echo "Testing HTTP response..."
curl http://localhost
Make it executable:

chmod +x deploy_test.sh
Step 3.2: Run the Script

./deploy_test.sh
Expected Output:

Deploying test page...
Restarting Apache...
Testing HTTP response...
<!DOCTYPE html>
<html>...</html>
Step 3.3: Verify via Browser

Open a browser and navigate to:

http://<your-server-IP>
Expected Outcome: The "Hello, Apache Server!" page appears.

