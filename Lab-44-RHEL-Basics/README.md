Lab 44: Managing SELinux Booleans and Policy Modules

Objectives

By the end of this lab, you will be able to:

View and modify SELinux booleans using getsebool and setsebool
Manage SELinux policies with semanage
Automate SELinux boolean management with a custom script
Understand how SELinux booleans affect system security
Prerequisites

Before starting, you should:

Have basic Linux command-line knowledge
Understand fundamental SELinux concepts (enforcing/permissive modes)
Use the provided Al Nafi Linux cloud machine (CentOS/RHEL 8/9 recommended)
Have sudo/root access to the machine
No need to set up a VM—just click Start Lab to begin!

Task 1: Managing SELinux Booleans

1.1 View Available Booleans

getsebool -a
Expected Output:
A list of all SELinux booleans with their current status (on/off).

Key Concept:
Booleans are toggle switches that modify SELinux policy behavior without rewriting rules.

1.2 Check a Boolean's Status

getsebool httpd_can_network_connect
Expected Output:
httpd_can_network_connect --> off (or current status)

1.3 Temporarily Change a Boolean

sudo setsebool httpd_can_network_connect on
Verify Change:
Run getsebool httpd_can_network_connect again to confirm.

Note: This change resets after reboot.

1.4 Make Changes Persistent

sudo setsebool -P httpd_can_network_connect on
Key Concept:
The -P flag writes changes to policy files, making them survive reboots.

Task 2: Modifying SELinux Policies

2.1 List All Boolean Descriptions

semanage boolean -l
Expected Output:
A table showing booleans with descriptions and current/static states.

2.2 Modify Boolean Default State

sudo semanage boolean --modify --on httpd_can_network_connect
Verify:
Check with semanage boolean -l | grep httpd_can_network_connect

Troubleshooting Tip:
If semanage isn't installed, run sudo dnf install policycoreutils-python-utils (RHEL/CentOS).

Task 3: Automating Boolean Management

3.1 Create a Boolean Management Script

nano selinux_booleans.sh
Paste this script:

#!/bin/bash
# Script to manage critical SELinux booleans

BOOLEANS=(
    "httpd_can_network_connect"
    "ftp_home_dir"
    "samba_export_all_rw"
)

for bool in "${BOOLEANS[@]}"; do
    CURRENT_STATE=$(getsebool "$bool" | awk '{print $3}')
    echo "Boolean: $bool (Current: $CURRENT_STATE)"
    
    read -p "Change? (y/n): " change
    if [ "$change" == "y" ]; then
        read -p "Enable? (on/off): " new_state
        sudo setsebool -P "$bool" "$new_state"
        echo "Changed $bool to $new_state"
    fi
done
3.2 Make Script Executable and Run

chmod +x selinux_booleans.sh
sudo ./selinux_booleans.sh
Example Workflow:

Script lists each boolean
Asks if you want to change it
Applies changes persistently
