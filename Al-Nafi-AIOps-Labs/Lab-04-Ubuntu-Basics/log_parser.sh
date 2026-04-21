#!/bin/bash
# Search for ERROR or WARNING in log file
echo "Errors and Warnings in system.log:"
grep -E "ERROR|WARNING" system.log
