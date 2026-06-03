Lab 87: Troubleshooting Nagios and NRPE

Objectives

By the end of this lab, you will be able to:

Identify common issues with Nagios and NRPE.
Use Nagios logs and NRPE debugging tools to diagnose problems.
Write a Bash script to monitor Nagios and NRPE services and report errors.
Prerequisites

A Linux system (Ubuntu/CentOS) with root/sudo access.
Nagios Core installed and configured.
NRPE (Nagios Remote Plugin Executor) installed on the local and remote hosts.
Basic knowledge of Linux commands and Bash scripting.
Task 1: Identify Common Issues with Nagios and NRPE

Subtask 1.1: List Common Nagios Issues

Common issues with Nagios include:

Service checks failing: Misconfigured plugins or incorrect check commands.
NRPE connection errors: Firewall blocking port 5666 or NRPE service not running.
Permission issues: Incorrect file permissions for plugins or configuration files.
Log file errors: Misconfigurations in nagios.cfg or nrpe.cfg.
Subtask 1.2: List Common NRPE Issues

Common NRPE issues include:

Connection refused: NRPE daemon not running or firewall blocking traffic.
Command not found: Plugin paths misconfigured in nrpe.cfg.
Timeout errors: Slow network or incorrect connection_timeout settings.
Task 2: Use Nagios Logs and NRPE Debugging Tools

Subtask 2.1: Check Nagios Logs

Open the Nagios log file:

sudo tail -f /var/log/nagios/nagios.log
Look for errors like CRITICAL, WARNING, or UNKNOWN states.
Check the Nagios debug log (if enabled in nagios.cfg):

sudo grep "debug" /var/log/nagios/nagios.debug
Expected Outcome:
You should see real-time logs indicating service checks, errors, or warnings.

Subtask 2.2: Debug NRPE Issues

Restart NRPE in debug mode:

sudo /usr/sbin/nrpe -c /etc/nagios/nrpe.cfg -d
Check for errors in the output.
Test NRPE connectivity from the Nagios server:

/usr/lib/nagios/plugins/check_nrpe -H <remote_host_ip>
If connection fails, check:
Firewall rules (sudo ufw status or sudo iptables -L).
NRPE service status (sudo systemctl status nrpe).
Expected Outcome:
A successful connection returns NRPE v4.x.x.

Task 3: Write a Script to Check Nagios and NRPE Status

Subtask 3.1: Create a Bash Script

Open a new file:

nano /usr/local/bin/check_nagios_nrpe.sh
Paste the following script:

#!/bin/bash

# Check Nagios service status
nagios_status=$(systemctl is-active nagios)
if [ "$nagios_status" != "active" ]; then
    echo "ERROR: Nagios service is $nagios_status"
    exit 1
fi

# Check NRPE service status
nrpe_status=$(systemctl is-active nrpe)
if [ "$nrpe_status" != "active" ]; then
    echo "ERROR: NRPE service is $nrpe_status"
    exit 1
fi

# Check Nagios log for errors
log_errors=$(sudo tail -n 50 /var/log/nagios/nagios.log | grep -E "CRITICAL|WARNING|UNKNOWN")
if [ -n "$log_errors" ]; then
    echo "ERROR: Nagios log contains issues:"
    echo "$log_errors"
    exit 1
fi

echo "SUCCESS: Nagios and NRPE are running without errors."
exit 0
Make the script executable:

sudo chmod +x /usr/local/bin/check_nagios_nrpe.sh
Subtask 3.2: Test the Script

Run the script:

/usr/local/bin/check_nagios_nrpe.sh
Expected Outcome:

If services are running, output: SUCCESS: Nagios and NRPE are running without errors.
If errors exist, the script reports them.
