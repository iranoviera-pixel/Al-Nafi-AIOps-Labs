Markdown
# Lab 33: Configuring DNS Server Addresses

## Objective
The goal of this lab is to manually configure and verify Domain Name System (DNS) resolution on an Ubuntu Linux system by modifying the `/etc/resolv.conf` file.

## Prerequisites
- Ubuntu 22.04 LTS or similar Linux distribution.
- Root or sudo privileges.
- Basic knowledge of the Linux terminal and text editors (nano).

## Tasks Completed

### Task 1: Backup and Edit DNS Configuration
1. **Backup Original Configuration:**
   Before making changes, the original configuration was backed up to prevent system network failure.
   ```bash
   sudo cp /etc/resolv.conf /etc/resolv.conf.bak
Configure DNS Nameservers:
Used nano to edit /etc/resolv.conf and added Google’s Public DNS servers to ensure reliable name resolution.

Plaintext
nameserver 8.8.8.8
nameserver 8.8.4.4
Task 2: Verification

Verify DNS Resolution:
Used the dig command to check the connectivity to root name servers and ensure the system can resolve external domains.

Bash
dig
Connectivity Test:
Verified internet access by pinging an external domain:

Bash
ping -c 4 google.com
Expected Outcome
After applying these changes, the system should successfully translate domain names (like github.com) into IP addresses, resolving the "Could not connect to server" errors encountered during Git operations.

Notes
In modern Ubuntu systems, /etc/resolv.conf is managed by systemd-resolved. While manual editing works for this lab, permanent changes should typically be configured via Netplan for production environments.


---

### **How to save this on your machine:**
1. Open a new file: `nano README.md`
2. Paste the text above.
3. Save and exit (**Ctrl+O**, **Enter**, **Ctrl+X**).
4. Now you can commit and push it:
   ```bash
   git add README.md
   git commit -m "Add documentation for Lab 33"
   git push origin main
