#!/bin/bash

# Define variables
REPO_DIR="/opt/myrepo"
REPO_FILE="/etc/yum.repos.d/myrepo.repo"

# Install createrepo if not present
if ! rpm -q createrepo; then
    yum install -y createrepo
fi

# Create repository directory
mkdir -p $REPO_DIR

# Generate metadata
createrepo $REPO_DIR

# Create repo file
cat > $REPO_FILE <<EOF
[myrepo]
name=My Custom Repository
baseurl=file://$REPO_DIR
enabled=1
gpgcheck=0
EOF

echo "Custom YUM repository setup complete!"

