#!/bin/bash
echo "=== Active Services ==="
systemctl list-units --type=service --state=running --no-pager


