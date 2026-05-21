Lab 65: Final Project - Linux Security Automation

Objectives

By the end of this lab, you will be able to:

Automate Linux security tasks including firewall configuration, antivirus scanning, rootkit detection, and SSH hardening.
Implement log and configuration change monitoring.
Test the security of the automated system using open-source tools.
Prerequisites

A Linux system (Ubuntu 20.04/22.04 recommended)
Basic knowledge of Linux command line
Sudo privileges on the system
Internet access for package installation
Lab Setup

Update your system:
sudo apt update && sudo apt upgrade -y
Install required packages:
sudo apt install -y ufw clamav rkhunter auditd fail2ban
Task 1: Security Automation Script

Subtask 1.1: Firewall Configuration with UFW

Enable and configure UFW (Uncomplicated Firewall):
sudo ufw enable
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
Verify the rules:
sudo ufw status verbose
Expected Output:

Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
Subtask 1.2: Antivirus Scanning with ClamAV

Update virus definitions:
sudo freshclam
Create a scan script (/usr/local/bin/clamscan_daily.sh):
#!/bin/bash
LOG_FILE="/var/log/clamav/scan_$(date +\%Y\%m\%d).log"
sudo clamscan -r / --exclude-dir=/sys/ --exclude-dir=/proc/ --exclude-dir=/dev/ -l "$LOG_FILE"
Make it executable:
sudo chmod +x /usr/local/bin/clamscan_daily.sh
Schedule daily scan (add to crontab):
(sudo crontab -l 2>/dev/null; echo "0 3 * * * /usr/local/bin/clamscan_daily.sh") | sudo crontab -
Subtask 1.3: Rootkit Detection with RKHunter

Update RKHunter:
sudo rkhunter --update
Configure RKHunter:
sudo rkhunter --propupd
Create scan script (/usr/local/bin/rkhunter_scan.sh):
#!/bin/bash
sudo rkhunter --check --sk --rwo
Schedule weekly scan:
(sudo crontab -l 2>/dev/null; echo "0 3 * * 0 /usr/local/bin/rkhunter_scan.sh") | sudo crontab -
Subtask 1.4: SSH Hardening

Edit SSH config:
sudo nano /etc/ssh/sshd_config
Add/modify these lines:
PermitRootLogin no
PasswordAuthentication no
MaxAuthTries 3
LoginGraceTime 60
Restart SSH:
sudo systemctl restart sshd
Task 2: Log and Configuration Monitoring

Subtask 2.1: Auditd Configuration

Enable auditd:
sudo systemctl enable --now auditd
Add rules for critical files:
sudo nano /etc/audit/rules.d/my.rules
Add:
-w /etc/passwd -p wa -k identity
-w /etc/ssh/sshd_config -p wa -k sshd
-w /var/log/auth.log -p wa -k authlog
Subtask 2.2: Fail2Ban Setup

Configure Fail2Ban for SSH:
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local
Modify:
[sshd]
enabled = true
maxretry = 3
bantime = 1h
Task 3: Security Testing

Subtask 3.1: Verify Firewall

sudo ufw status
Expected: SSH port should be the only allowed incoming port.

Subtask 3.2: Test ClamAV

sudo clamscan --infected --remove --recursive /tmp
Expected: No infected files found.

Subtask 3.3: Test RKHunter

sudo rkhunter --check --sk
Expected: No warnings should appear.

Subtask 3.4: Test SSH Security

Attempt SSH with:

ssh root@localhost
Expected: Connection should be refused.
