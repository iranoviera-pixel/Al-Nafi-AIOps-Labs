Lab 42: Configuring OpenSCAP Profiles

Objectives

By the end of this lab, students will be able to:

Install and configure OpenSCAP on a Linux system.
Run predefined security profiles to assess system compliance.
Automate OpenSCAP policy application using a Bash script.
Interpret scan results to identify security vulnerabilities.
Prerequisites

Before starting this lab, ensure you have:

A Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Basic familiarity with Linux command-line operations.
Sudo or root privileges to install packages and modify system configurations.
Task 1: Install and Configure OpenSCAP

Step 1: Update System Packages

Open a terminal and run:

sudo apt update && sudo apt upgrade -y
Expected Outcome: All system packages are updated.

Step 2: Install OpenSCAP Tools

Install the OpenSCAP scanner and utilities:

sudo apt install -y openscap-scanner scap-security-guide
Expected Outcome: OpenSCAP and security profiles are installed.

Step 3: Verify Installation

Check the installed version:

oscap --version
Expected Outcome: Output shows the OpenSCAP version (e.g., 1.3.7).

Task 2: Run Predefined Security Profiles

Step 1: List Available Profiles

View predefined SCAP profiles:

oscap info /usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml
Expected Outcome: A list of profiles (e.g., cis_level1_server, pci-dss).

Step 2: Run a Basic Compliance Scan

Scan the system using the cis_level1_server profile:

sudo oscap xccdf eval --profile cis_level1_server \
--results scan_results.xml \
/usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml
Expected Outcome: A report (scan_results.xml) is generated in the current directory.

Step 3: Generate a Human-Readable Report

Convert the XML report to HTML:

oscap xccdf generate report scan_results.xml > scan_report.html
Expected Outcome: An HTML file (scan_report.html) is created. Open it in a browser to view findings.

Troubleshooting Tip: If the command fails, ensure libxslt is installed (sudo apt install libxslt1.1).

Task 3: Automate OpenSCAP Policy Application

Step 1: Create a Bash Script

Write a script (apply_oscap.sh) to automate scans:

#!/bin/bash
PROFILE="cis_level1_server"
SCAP_FILE="/usr/share/xml/scap/ssg/content/ssg-ubuntu2204-ds.xml"
OUTPUT_FILE="scan_results_$(date +%F).xml"

echo "Running OpenSCAP scan with profile: $PROFILE"
sudo oscap xccdf eval --profile "$PROFILE" --results "$OUTPUT_FILE" "$SCAP_FILE"

echo "Generating HTML report..."
oscap xccdf generate report "$OUTPUT_FILE" > "scan_report_$(date +%F).html"

echo "Scan complete. Report saved as scan_report_$(date +%F).html"
Step 2: Make the Script Executable

chmod +x apply_oscap.sh
Step 3: Run the Script

./apply_oscap.sh
Expected Outcome: The script runs a scan and generates a timestamped report.
