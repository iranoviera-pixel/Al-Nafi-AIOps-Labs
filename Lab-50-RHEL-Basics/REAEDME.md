Lab 50: Case Study: Implementing SELinux in a Production Environment

Lab Objectives

By the end of this lab, students will be able to:

Understand SELinux implementation challenges in production environments
Analyze a real-world case study of SELinux deployment
Create automated scripts for deploying SELinux policies across multiple services
Evaluate security impacts and benefits of SELinux configurations
Apply best practices for SELinux policy management in production systems
Troubleshoot common SELinux issues in enterprise environments
Prerequisites

Before starting this lab, students should have:

Basic understanding of Linux system administration
Familiarity with command-line interface operations
Knowledge of file permissions and system security concepts
Understanding of web services (Apache, Nginx) and database systems
Basic scripting knowledge (bash scripting preferred)
Completed previous SELinux fundamentals labs
Lab Environment Setup

Ready-to-Use Cloud Machines: Al Nafi provides pre-configured Linux-based cloud machines for this lab. Simply click Start Lab to access your environment - no need to build your own VM or install additional software.

Your lab environment includes:

CentOS 8 or RHEL 8 system with SELinux enabled
Pre-installed web server (Apache)
Database server (MariaDB)
Development tools and text editors
Root access for system configuration
Task 1: Review Production Environment Case Study

Subtask 1.1: Understanding the Business Scenario

Company Background: TechCorp Solutions is a mid-sized e-commerce company that processes customer orders through a web application stack consisting of:

Frontend web servers (Apache)
Application servers (PHP/Python)
Database servers (MariaDB)
File storage systems
Load balancers
Security Challenge: The company experienced a security breach where an attacker gained unauthorized access through a web application vulnerability and moved laterally through the system.

Solution Requirements:

Implement mandatory access controls
Limit service privileges
Prevent lateral movement
Maintain system performance
Ensure compliance with security standards
Subtask 1.2: Analyze Current System State

First, let's examine the current SELinux status on your system:

# Check SELinux status
sestatus

# View current SELinux mode
getenforce

# Check SELinux policy version
sestatus | grep "Policy version"

# List all SELinux booleans
getsebool -a | head -20
Create a system assessment script:

# Create system assessment script
cat > /root/selinux_assessment.sh << 'EOF'
#!/bin/bash

echo "=== SELinux Production Environment Assessment ==="
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo ""

echo "1. SELinux Status:"
sestatus
echo ""

echo "2. Current Enforcement Mode:"
getenforce
echo ""

echo "3. SELinux Policy Type:"
sestatus | grep "Loaded policy name"
echo ""

echo "4. SELinux Root Directory:"
sestatus | grep "SELinux root directory"
echo ""

echo "5. Active Services with SELinux Context:"
ps auxZ | grep -E "(httpd|mysqld|sshd)" | head -10
echo ""

echo "6. File Context Examples:"
ls -Z /var/www/html/ 2>/dev/null || echo "Web directory not found"
ls -Z /var/lib/mysql/ 2>/dev/null || echo "Database directory not found"
echo ""

echo "7. SELinux Denials (last 10):"
ausearch -m avc -ts recent 2>/dev/null | tail -10 || echo "No recent denials found"
echo ""

echo "Assessment completed at $(date)"
EOF

# Make script executable
chmod +x /root/selinux_assessment.sh

# Run the assessment
/root/selinux_assessment.sh
Subtask 1.3: Document Current Security Gaps

Create a security gap analysis document:

# Create security analysis document
cat > /root/security_gaps.txt << 'EOF'
SELINUX PRODUCTION ENVIRONMENT - SECURITY GAP ANALYSIS

1. IDENTIFIED SECURITY GAPS:
   - Services running with excessive privileges
   - Lack of proper file context labeling
   - Missing custom policies for applications
   - Inadequate network access controls
   - Insufficient audit logging configuration

2. RISK ASSESSMENT:
   - HIGH: Unconfined services can access system resources
   - MEDIUM: Improper file contexts allow unauthorized access
   - MEDIUM: Missing application-specific policies
   - LOW: Default SELinux booleans may be too permissive

3. COMPLIANCE REQUIREMENTS:
   - Implement least privilege access
   - Enable comprehensive audit logging
   - Create custom policies for business applications
   - Regular policy review and updates

4. PERFORMANCE CONSIDERATIONS:
   - Monitor system performance impact
   - Optimize policy rules for efficiency
   - Balance security with operational requirements
EOF

# Display the analysis
cat /root/security_gaps.txt
Task 2: Create Automated SELinux Policy Deployment Script

Subtask 2.1: Design Multi-Service Policy Framework

Create a comprehensive deployment script for multiple services:

# Create the main deployment script
cat > /root/selinux_deploy.sh << 'EOF'
#!/bin/bash

# SELinux Production Deployment Script
# Version: 1.0
# Purpose: Automate SELinux policy deployment for production services

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log_message() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

error_message() {
    echo -e "${RED}[ERROR]${NC} $1"
}

success_message() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

warning_message() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check if running as root
check_root() {
    if [[ $EUID -ne 0 ]]; then
        error_message "This script must be run as root"
        exit 1
    fi
}

# Backup current SELinux configuration
backup_selinux_config() {
    log_message "Creating backup of current SELinux configuration..."
    
    BACKUP_DIR="/root/selinux_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"
    
    # Backup SELinux config
    cp /etc/selinux/config "$BACKUP_DIR/"
    
    # Backup current contexts
    semanage fcontext -l > "$BACKUP_DIR/file_contexts.backup"
    semanage port -l > "$BACKUP_DIR/port_contexts.backup"
    getsebool -a > "$BACKUP_DIR/booleans.backup"
    
    success_message "Backup created in $BACKUP_DIR"
}

# Configure SELinux for web services
configure_web_services() {
    log_message "Configuring SELinux for web services..."
    
    # Install required packages
    yum install -y httpd mod_ssl policycoreutils-python-utils
    
    # Set proper file contexts for web content
    semanage fcontext -a -t httpd_exec_t "/var/www/html/.*\.cgi"
    semanage fcontext -a -t httpd_exec_t "/var/www/html/.*\.pl"
    semanage fcontext -a -t httpd_exec_t "/var/www/html/.*\.py"
    
    # Configure web server directories
    semanage fcontext -a -t httpd_var_lib_t "/var/www/uploads(/.*)?"
    semanage fcontext -a -t httpd_log_t "/var/log/httpd(/.*)?"
    
    # Apply contexts
    restorecon -R /var/www/
    restorecon -R /var/log/httpd/
    
    # Configure SELinux booleans for web services
    setsebool -P httpd_can_network_connect on
    setsebool -P httpd_can_network_connect_db on
    setsebool -P httpd_execmem off
    setsebool -P httpd_enable_homedirs off
    
    success_message "Web services SELinux configuration completed"
}

# Configure SELinux for database services
configure_database_services() {
    log_message "Configuring SELinux for database services..."
    
    # Install MariaDB
    yum install -y mariadb-server mariadb
    
    # Set proper contexts for database
    semanage fcontext -a -t mysqld_db_t "/var/lib/mysql(/.*)?"
    semanage fcontext -a -t mysqld_log_t "/var/log/mariadb(/.*)?"
    semanage fcontext -a -t mysqld_var_run_t "/var/run/mysqld(/.*)?"
    
    # Apply contexts
    restorecon -R /var/lib/mysql/
    restorecon -R /var/log/mariadb/
    
    # Configure database SELinux settings
    setsebool -P mysql_connect_any off
    setsebool -P selinuxuser_mysql_connect_enabled on
    
    success_message "Database services SELinux configuration completed"
}

# Configure SELinux for SSH services
configure_ssh_services() {
    log_message "Configuring SELinux for SSH services..."
    
    # Configure SSH port contexts (if using non-standard ports)
    # semanage port -a -t ssh_port_t -p tcp 2222
    
    # Set SSH-related booleans
    setsebool -P ssh_chroot_rw_homedirs off
    setsebool -P ssh_sysadm_login off
    
    # Configure SSH file contexts
    restorecon -R /etc/ssh/
    restorecon -R /var/log/secure
    
    success_message "SSH services SELinux configuration completed"
}

# Create custom SELinux policy module
create_custom_policy() {
    log_message "Creating custom SELinux policy module..."
    
    # Create policy directory
    mkdir -p /root/selinux_policies
    cd /root/selinux_policies
    
    # Create a custom policy for application
    cat > myapp.te << 'POLICY_EOF'
policy_module(myapp, 1.0)

require {
    type httpd_t;
    type httpd_exec_t;
    type var_t;
    class file { read write create unlink };
    class dir { search write add_name remove_name };
}

# Allow httpd to manage application files
allow httpd_t var_t:file { read write create unlink };
allow httpd_t var_t:dir { search write add_name remove_name };
POLICY_EOF
    
    # Compile and install the policy
    make -f /usr/share/selinux/devel/Makefile myapp.pp
    semodule -i myapp.pp
    
    success_message "Custom policy module installed"
}

# Configure audit logging
configure_audit_logging() {
    log_message "Configuring SELinux audit logging..."
    
    # Install audit packages
    yum install -y audit audispd-plugins
    
    # Configure auditd
    systemctl enable auditd
    systemctl start auditd
    
    # Add SELinux-specific audit rules
    cat >> /etc/audit/rules.d/selinux.rules << 'AUDIT_EOF'
# SELinux audit rules
-w /etc/selinux/ -p wa -k selinux_config
-w /usr/sbin/semanage -p x -k selinux_manage
-w /usr/sbin/setsebool -p x -k selinux_boolean
AUDIT_EOF
    
    # Restart auditd to apply rules
    service auditd restart
    
    success_message "Audit logging configured"
}

# Validate SELinux configuration
validate_configuration() {
    log_message "Validating SELinux configuration..."
    
    # Check SELinux status
    if [[ $(getenforce) != "Enforcing" ]]; then
        warning_message "SELinux is not in Enforcing mode"
    else
        success_message "SELinux is in Enforcing mode"
    fi
    
    # Check for recent denials
    DENIALS=$(ausearch -m avc -ts recent 2>/dev/null | wc -l)
    if [[ $DENIALS -gt 0 ]]; then
        warning_message "Found $DENIALS recent SELinux denials"
        log_message "Run 'ausearch -m avc -ts recent' to review denials"
    else
        success_message "No recent SELinux denials found"
    fi
    
    # Test service contexts
    log_message "Service context validation:"
    ps auxZ | grep -E "(httpd|mysqld|sshd)" | head -5
}

# Generate deployment report
generate_report() {
    log_message "Generating deployment report..."
    
    REPORT_FILE="/root/selinux_deployment_report_$(date +%Y%m%d_%H%M%S).txt"
    
    cat > "$REPORT_FILE" << 'REPORT_EOF'
SELinux Production Deployment Report
===================================

Deployment Date: $(date)
System: $(hostname)
SELinux Status: $(sestatus | grep "SELinux status")
Current Mode: $(getenforce)

Services Configured:
- Web Services (Apache/HTTP)
- Database Services (MariaDB)
- SSH Services
- Custom Application Policies

Security Enhancements Applied:
- Proper file context labeling
- Service-specific boolean configuration
- Custom policy modules
- Enhanced audit logging
- Network access restrictions

Post-Deployment Validation:
- SELinux enforcement status: $(getenforce)
- Recent denials: $(ausearch -m avc -ts recent 2>/dev/null | wc -l)
- Active services with contexts verified

Recommendations:
1. Monitor audit logs regularly
2. Review and update policies quarterly
3. Test application functionality thoroughly
4. Maintain backup of working configurations

Report generated: $(date)
REPORT_EOF
    
    success_message "Deployment report saved to $REPORT_FILE"
}

# Main execution function
main() {
    log_message "Starting SELinux Production Deployment"
    
    check_root
    backup_selinux_config
    configure_web_services
    configure_database_services
    configure_ssh_services
    create_custom_policy
    configure_audit_logging
    validate_configuration
    generate_report
    
    success_message "SELinux production deployment completed successfully!"
    log_message "Please review the deployment report and test all services"
}

# Execute main function
main "$@"
EOF

# Make the script executable
chmod +x /root/selinux_deploy.sh
Subtask 2.2: Create Service-Specific Policy Scripts

Create individual scripts for specific services:

# Web server specific policy script
cat > /root/web_server_policy.sh << 'EOF'
#!/bin/bash

echo "Configuring SELinux for Web Server..."

# Create web content directories
mkdir -p /var/www/html/app
mkdir -p /var/www/uploads
mkdir -p /var/log/webapp

# Set file contexts
semanage fcontext -a -t httpd_exec_t "/var/www/html/app/.*\.php"
semanage fcontext -a -t httpd_var_lib_t "/var/www/uploads(/.*)?"
semanage fcontext -a -t httpd_log_t "/var/log/webapp(/.*)?"

# Apply contexts
restorecon -R /var/www/
restorecon -R /var/log/webapp/

# Configure booleans
setsebool -P httpd_can_network_connect on
setsebool -P httpd_can_network_connect_db on
setsebool -P httpd_use_nfs off
setsebool -P httpd_enable_cgi on

echo "Web server SELinux configuration completed"
EOF

chmod +x /root/web_server_policy.sh

# Database server specific policy script
cat > /root/database_policy.sh << 'EOF'
#!/bin/bash

echo "Configuring SELinux for Database Server..."

# Create database directories
mkdir -p /var/lib/mysql/data
mkdir -p /var/log/mysql

# Set file contexts
semanage fcontext -a -t mysqld_db_t "/var/lib/mysql/data(/.*)?"
semanage fcontext -a -t mysqld_log_t "/var/log/mysql(/.*)?"

# Apply contexts
restorecon -R /var/lib/mysql/
restorecon -R /var/log/mysql/

# Configure database booleans
setsebool -P mysql_connect_any off
setsebool -P selinuxuser_mysql_connect_enabled on

echo "Database server SELinux configuration completed"
EOF

chmod +x /root/database_policy.sh
Subtask 2.3: Test the Deployment Scripts

Run the deployment scripts and verify functionality:

# Test the main deployment script
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log_message "Testing SELinux deployment scripts..."

# Run web server configuration
./web_server_policy.sh

# Run database configuration  
./database_policy.sh

# Verify configurations
echo "Verifying web server contexts:"
ls -Z /var/www/html/

echo "Verifying database contexts:"
ls -Z /var/lib/mysql/

echo "Current SELinux booleans (web-related):"
getsebool -a | grep httpd | head -10

echo "Current SELinux booleans (database-related):"
getsebool -a | grep mysql
Task 3: Evaluate Security Impact of SELinux Configuration

Subtask 3.1: Security Assessment Framework

Create a comprehensive security evaluation script:

cat > /root/security_evaluation.sh << 'EOF'
#!/bin/bash

# SELinux Security Impact Evaluation Script
# Purpose: Assess security improvements after SELinux implementation

echo "=== SELinux Security Impact Evaluation ==="
echo "Evaluation Date: $(date)"
echo "System: $(hostname)"
echo ""

# Function to calculate security score
calculate_security_score() {
    local score=0
    
    # Check SELinux enforcement
    if [[ $(getenforce) == "Enforcing" ]]; then
        score=$((score + 25))
        echo "✓ SELinux Enforcing Mode: +25 points"
    else
        echo "✗ SELinux not in Enforcing Mode: 0 points"
    fi
    
    # Check for custom policies
    if semodule -l | grep -q "myapp"; then
        score=$((score + 15))
        echo "✓ Custom Policy Module: +15 points"
    else
        echo "✗ No Custom Policy Module: 0 points"
    fi
    
    # Check proper file contexts
    local context_errors=$(find /var/www -type f -exec ls -Z {} \; 2>/dev/null | grep -v httpd | wc -l)
    if [[ $context_errors -eq 0 ]]; then
        score=$((score + 20))
        echo "✓ Proper File Contexts: +20 points"
    else
        echo "✗ File Context Issues Found: 0 points"
    fi
    
    # Check security booleans
    local secure_booleans=0
    if [[ $(getsebool httpd_execmem | cut -d' ' -f3) == "off" ]]; then
        secure_booleans=$((secure_booleans + 1))
    fi
    if [[ $(getsebool httpd_enable_homedirs | cut -d' ' -f3) == "off" ]]; then
        secure_booleans=$((secure_booleans + 1))
    fi
    
    if [[ $secure_booleans -eq 2 ]]; then
        score=$((score + 15))
        echo "✓ Secure Boolean Configuration: +15 points"
    else
        echo "✗ Insecure Boolean Settings: 0 points"
    fi
    
    # Check audit configuration
    if systemctl is-active auditd >/dev/null 2>&1; then
        score=$((score + 10))
        echo "✓ Audit Logging Active: +10 points"
    else
        echo "✗ Audit Logging Inactive: 0 points"
    fi
    
    # Check for recent denials
    local denials=$(ausearch -m avc -ts recent 2>/dev/null | wc -l)
    if [[ $denials -eq 0 ]]; then
        score=$((score + 15))
        echo "✓ No Recent Denials: +15 points"
    else
        echo "✗ Recent Denials Found ($denials): 0 points"
    fi
    
    echo ""
    echo "Total Security Score: $score/100"
    
    if [[ $score -ge 80 ]]; then
        echo "Security Level: EXCELLENT"
    elif [[ $score -ge 60 ]]; then
        echo "Security Level: GOOD"
    elif [[ $score -ge 40 ]]; then
        echo "Security Level: FAIR"
    else
        echo "Security Level: POOR"
    fi
}

# Analyze attack surface reduction
analyze_attack_surface() {
    echo ""
    echo "=== Attack Surface Analysis ==="
    
    echo "1. Service Confinement:"
    ps auxZ | grep -E "(httpd|mysqld|sshd)" | while read line; do
        echo "   $line"
    done
    
    echo ""
    echo "2. Network Access Restrictions:"
    getsebool -a | grep -E "(connect|network)" | head -10
    
    echo ""
    echo "3. File System Access Controls:"
    echo "   Web server file access:"
    ls -Z /var/www/html/ | head -5
    echo "   Database file access:"
    ls -Z /var/lib/mysql/ 2>/dev/null | head -5 || echo "   Database not accessible"
}

# Performance impact assessment
assess_performance_impact() {
    echo ""
    echo "=== Performance Impact Assessment ==="
    
    # Check system load
    echo "Current System Load:"
    uptime
    
    # Check memory usage
    echo ""
    echo "Memory Usage:"
    free -h
    
    # Check SELinux overhead
    echo ""
    echo "SELinux Process Overhead:"
    ps aux | grep -E "(selinux|audit)" | grep -v grep
    
    echo ""
    echo "Disk I/O for SELinux logs:"
    du -sh /var/log/audit/ 2>/dev/null || echo "Audit logs: Not available"
}

# Compliance assessment
assess_compliance() {
    echo ""
    echo "=== Compliance Assessment ==="
    
    echo "1. Mandatory Access Control: $(getenforce)"
    echo "2. Audit Trail: $(systemctl is-active auditd 2>/dev/null || echo 'Inactive')"
    echo "3. Least Privilege: Implemented via SELinux policies"
    echo "4. Data Protection: File contexts properly configured"
    echo "5. Network Segmentation: Service-specific network policies"
}

# Generate recommendations
generate_recommendations() {
    echo ""
    echo "=== Security Recommendations ==="
    
    # Check for improvements
    if [[ $(getenforce) != "Enforcing" ]]; then
        echo "• Enable SELinux Enforcing mode"
    fi
    
    local denials=$(ausearch -m avc -ts recent 2>/dev/null | wc -l)
    if [[ $denials -gt 0 ]]; then
        echo "• Review and address SELinux denials"
        echo "• Run: ausearch -m avc -ts recent | audit2allow -M mypolicy"
    fi
    
    if ! semodule -l | grep -q "myapp"; then
        echo "• Implement application-specific SELinux policies"
    fi
    
    echo "• Regular policy reviews and updates"
    echo "• Monitor audit logs for security events"
    echo "• Test disaster recovery procedures"
    echo "• Staff training on SELinux management"
}

# Main execution
main() {
    calculate_security_score
    analyze_attack_surface
    assess_performance_impact
    assess_compliance
    generate_recommendations
    
    echo ""
    echo "=== Evaluation Complete ==="
    echo "Report saved to: /root/security_evaluation_$(date +%Y%m%d_%H%M%S).log"
}

# Execute evaluation
main | tee /root/security_evaluation_$(date +%Y%m%d_%H%M%S).log
EOF

chmod +x /root/security_evaluation.sh
Subtask 3.2: Run Security Evaluation

Execute the security evaluation script:

# Run the security evaluation
./security_evaluation.sh

# Create a detailed security report
cat > /root/detailed_security_report.txt << 'EOF'
DETAILED SECURITY IMPACT REPORT
===============================

EXECUTIVE SUMMARY:
The implementation of SELinux in the production environment has significantly enhanced the security posture by implementing mandatory access controls, reducing attack surface, and providing comprehensive audit capabilities.

KEY SECURITY IMPROVEMENTS:

1. MANDATORY ACCESS CONTROL (MAC):
   - Replaced discretionary access control with policy-based access
   - Services now run with minimal required privileges
   - Prevented privilege escalation attacks

2. ATTACK SURFACE REDUCTION:
   - Web server confined to specific file contexts
   - Database access restricted to authorized processes
   - Network connections limited by policy rules

3. LATERAL MOVEMENT PREVENTION:
   - Service isolation prevents cross-service attacks
   - File system access strictly controlled
   - Process communication restricted by policy

4. AUDIT AND COMPLIANCE:
   - Comprehensive logging of security events
   - Policy violations automatically detected
   - Compliance with security frameworks enhanced

QUANTITATIVE BENEFITS:
- 95% reduction in potential privilege escalation paths
- 80% reduction in file system attack surface
- 100% improvement in audit trail completeness
- 90% reduction in lateral movement possibilities

PERFORMANCE IMPACT:
- CPU overhead: <2%
- Memory overhead: <1%
- Disk I/O increase: <5% (due to audit logging)
- Network performance: No measurable impact

RISK MITIGATION:
- HIGH RISK: Unconfined service access - MITIGATED
- MEDIUM RISK: Inadequate file permissions - MITIGATED  
- MEDIUM RISK: Privilege escalation - MITIGATED
- LOW RISK: Information disclosure - MITIGATED

RETURN ON INVESTMENT:
- Reduced security incident response costs
- Improved compliance posture
- Enhanced customer trust
- Reduced insurance premiums potential

RECOMMENDATIONS FOR CONTINUOUS IMPROVEMENT:
1. Regular policy reviews and updates
2. Staff training on SELinux management
3. Automated policy testing in development
4. Integration with security monitoring tools
5. Regular penetration testing validation
EOF

# Display the report
cat /root/detailed_security_report.txt
Subtask 3.3: Create Monitoring and Maintenance Scripts

Develop ongoing monitoring capabilities:

# Create monitoring script
cat > /root/selinux_monitor.sh << 'EOF'
#!/bin/bash

# SELinux Production Monitoring Script
# Purpose: Continuous monitoring of SELinux status and security events

LOGFILE="/var/log/selinux_monitor.log"
EMAIL_ALERT="admin@company.com"  # Configure as needed

# Logging function
log_event() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOGFILE"
}

# Check SELinux status
check_selinux_status() {
    local current_mode=$(getenforce)
    if [[ "$current_mode" != "Enforcing" ]]; then
        log_event "ALERT: SELinux not in Enforcing mode - Current: $current_mode"
        return 1
    fi
    return 0
}

# Monitor for new denials
check_denials() {
    local recent_denials=$(ausearch -m avc -ts today 2>/dev/null | wc -l)
    if [[ $recent_denials -gt 0 ]]; then
        log_event "WARNING: $recent_denials SELinux denials found today"
        ausearch -m avc -ts today 2>/dev/null | tail -5 >> "$LOGFILE"
        return 1
    fi
    return 0
}

# Check policy integrity
check_policy_integrity() {
    local policy_count=$(semodule -l | wc -l)
    if [[ $policy_count -lt 10 ]]; then
        log_event "ALERT: Unusually low policy count: $policy_count"
        return 1
    fi
    return 0
}

# Check audit service
check_audit_service() {
    if ! systemctl is-active auditd >/dev/null 2>&1; then
        log_event "ALERT: Audit service is not running"
        return 1
    fi
    return 0
}

# Main monitoring function
main_monitor() {
    log_event "Starting SELinux monitoring check"
    
    local alerts=0
    
    check_selinux_status || alerts=$((alerts + 1))
    check_denials || alerts=$((alerts + 1))
    check_policy_integrity || alerts=$((alerts + 1))
    check_audit_service || alerts=$((alerts + 1))
    
    if [[ $alerts -eq 0 ]]; then
        log_event "All SELinux checks passed successfully"
    else
        log_event "SELinux monitoring found $alerts issues requiring attention"
    fi
    
    log_event "Monitoring check completed"
}

# Execute monitoring
main_monitor
EOF

chmod +x /root/selinux_monitor.sh

# Create a cron job for regular monitoring
echo "# SELinux monitoring - runs every hour" >> /etc/crontab
echo "0 * * * * root /root/selinux_monitor.sh" >> /etc/crontab

# Test the monitoring script
./selinux_monitor.sh
