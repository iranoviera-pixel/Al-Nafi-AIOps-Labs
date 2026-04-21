#!/bin/bash

# =================================================================
# Script Name   : package_manager.sh
# Description   : Linux Package Management Automation (AIOps Lab)
# Author        : iranoviera-pixel
# College       : Al Nafi International College (EduQual Level 6)
# =================================================================

# Warna untuk output agar mudah dibaca
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}--- Starting Package Management Task ---${NC}"

# 1. Update system repositories
echo -e "${GREEN}[1/3] Updating System Repositories...${NC}"
sudo yum update -y

# 2. Check if a specific package is installed (Example: wget)
PACKAGE="wget"
echo -e "${GREEN}[2/3] Checking for package: $PACKAGE...${NC}"

if rpm -q $PACKAGE &>/dev/null; then
    echo -e "${BLUE}$PACKAGE is already installed.${NC}"
else
    echo -e "${BLUE}$PACKAGE not found. Installing now...${NC}"
    sudo yum install -y $PACKAGE
fi

# 3. List recently installed packages
echo -e "${GREEN}[3/3] Task Complete. System is ready.${NC}"
echo "Current Date: $(date)"

echo -e "${BLUE}--- End of Script ---${NC}"
