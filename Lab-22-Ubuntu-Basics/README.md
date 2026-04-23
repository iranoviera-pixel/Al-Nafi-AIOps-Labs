# Lab 22: System Performance Reporting and Monitoring

This repository documents the practical implementation of system monitoring and automated reporting on a Linux environment. The lab covers real-time analysis, historical data collection, and the automation of performance logs using Bash scripting and Cron.

## Objectives
* Install and utilize advanced system monitoring tools (`htop`, `sysstat`).
* Analyze real-time and historical system statistics.
* Develop a Bash script to automate performance data collection into CSV format.
* Implement automated scheduling using Cron jobs.

---

## Task 1: Installing and Exploring Monitoring Tools

### 1.1 Tool Installation
Necessary utilities were installed to provide both interactive and statistical insights.
```bash
# For Debian/Ubuntu-based systems
sudo apt update
sudo apt install -y htop sysstat


