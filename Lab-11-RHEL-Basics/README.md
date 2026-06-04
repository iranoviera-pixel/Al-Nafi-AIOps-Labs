Lab 11: Managing Local Users and Groups

Objectives

By the end of this lab, you will be able to:

Create and manage local users and groups using command-line tools.
Modify user attributes with usermod.
Automate user and group management tasks using a Bash script.
Prerequisites

Before starting, ensure you have:

Basic familiarity with Linux command line.
Access to a Linux-based system (Al Nafi provides pre-configured cloud machines—click Start Lab to begin).
Administrative/sudo privileges (required for user/group management commands).
Task 1: Create Local Users and Groups

Step 1: Create a New Group

Use groupadd to create a group named developers:

sudo groupadd developers
Expected Output: No output indicates success. Verify with:

getent group developers
Troubleshooting: If you see "group already exists", choose a different group name.

Step 2: Create a New User

Use useradd to create a user named alice and assign her to developers:

sudo useradd -m -G developers alice
-m: Creates a home directory.
-G: Adds the user to the developers group.
Verify:

id alice
Expected Output: Shows alice’s UID and group memberships.

Task 2: Modify User Details

Step 1: Change User’s Primary Group

Use usermod to set developers as alice’s primary group:

sudo usermod -g developers alice
Verify:

id alice
Expected Output: gid should now match the developers group ID.

Step 2: Add a Comment to User

Add a description (e.g., "Dev Team Lead"):

sudo usermod -c "Dev Team Lead" alice
Verify:

grep alice /etc/passwd
Expected Output: Displays the comment in the user’s entry.

Task 3: Automate Group/User Creation with a Script

Step 1: Create a User List File

Create userlist.txt with the following content (one username per line):

bob
charlie
dave
Step 2: Write the Script

Create add_users.sh with the following code:

#!/bin/bash
GROUP="developers"  # Group name
USERFILE="userlist.txt"  # File containing usernames

# Create group if it doesn’t exist
sudo groupadd $GROUP 2>/dev/null

# Add each user to the group
while read USER; do
  sudo useradd -m -G $GROUP $USER
  echo "Added $USER to $GROUP"
done < $USERFILE
Step 3: Run the Script

Make the script executable and run it:

chmod +x add_users.sh
sudo ./add_users.sh
Expected Output:

Added bob to developers
Added charlie to developers
Added dave to developers
Verify with:

getent group developers
