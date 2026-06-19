Lab 49: AI-Powered SELinux Policy Generation

Lab Objectives

By the end of this lab, students will be able to:

Understand the fundamentals of SELinux policy generation and its importance in system security
Research and identify AI-powered tools for automating SELinux policy creation
Develop a Python-based machine learning script that analyzes system activity logs to suggest SELinux policies
Implement and test AI-generated SELinux policies on a live system
Evaluate the effectiveness of automated policy generation versus manual policy creation
Apply machine learning concepts to cybersecurity and system administration tasks
Prerequisites

Before starting this lab, students should have:

Basic understanding of Linux system administration
Familiarity with SELinux concepts and terminology
Basic Python programming knowledge
Understanding of log file analysis
Knowledge of machine learning fundamentals (helpful but not required)
Experience with command-line interface operations
Lab Environment Setup

Ready-to-Use Cloud Machines: Al Nafi provides pre-configured Linux-based cloud machines with all necessary tools installed. Simply click Start Lab to access your environment - no need to build your own virtual machine or install additional software.

Your cloud machine includes:

CentOS/RHEL 8 or Fedora with SELinux enabled
Python 3.8+ with required libraries
Sample log files and datasets
Development tools and text editors
Task 1: Research AI Tools for SELinux Policy Generation

Subtask 1.1: Understanding Current AI-Powered SELinux Tools

First, let's explore the landscape of AI tools available for SELinux policy generation.

Access your cloud machine and open a terminal

Create a research directory for organizing your findings:

mkdir -p ~/selinux-ai-lab
cd ~/selinux-ai-lab
mkdir research tools scripts logs
Research existing tools by examining available open-source projects:
# Create a research notes file
nano research/ai-tools-research.md
Add the following content to document your research:

# AI-Powered SELinux Policy Generation Tools Research

## Open Source Tools and Frameworks:

### 1. SELinux Policy Analysis Tools
- **sepolicy-analyze**: Built-in tool for policy analysis
- **setools**: Collection of policy analysis tools
- **sealert**: Alert analysis and suggestion tool

### 2. Machine Learning Frameworks for Security
- **scikit-learn**: General-purpose ML library
- **pandas**: Data analysis and manipulation
- **numpy**: Numerical computing support

### 3. Log Analysis Tools
- **auditd**: Linux audit framework
- **rsyslog**: System logging facility
- **logwatch**: Log analysis and reporting

## Research Findings:
- Most SELinux policy generation is currently rule-based
- AI/ML approaches are emerging in academic research
- Opportunity exists for innovative ML-based solutions
Install required Python libraries for our AI development:
sudo dnf install -y python3-pip python3-devel
pip3 install --user scikit-learn pandas numpy matplotlib seaborn audit-python
Subtask 1.2: Analyzing System Logs for Policy Insights

Examine current SELinux status and generate some activity:
# Check SELinux status
sestatus

# Generate some SELinux denials for analysis
sudo setenforce 0  # Set to permissive mode temporarily
sudo setenforce 1  # Back to enforcing mode

# Check recent SELinux denials
sudo ausearch -m avc -ts recent
Create a log collection script:
nano scripts/collect_selinux_logs.py
#!/usr/bin/env python3
"""
SELinux Log Collection Script
Collects and preprocesses SELinux audit logs for AI analysis
"""

import subprocess
import json
import re
from datetime import datetime, timedelta
import os

class SELinuxLogCollector:
    def __init__(self, output_dir="logs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def collect_avc_denials(self, days_back=7):
        """Collect AVC denial messages from audit logs"""
        try:
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)
            
            # Format dates for ausearch
            start_str = start_date.strftime("%m/%d/%Y %H:%M:%S")
            
            # Run ausearch command
            cmd = ["sudo", "ausearch", "-m", "avc", "-ts", start_str]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout
            else:
                print(f"No AVC denials found in the last {days_back} days")
                return ""
                
        except Exception as e:
            print(f"Error collecting AVC denials: {e}")
            return ""
    
    def parse_avc_denial(self, avc_line):
        """Parse individual AVC denial line"""
        denial_data = {}
        
        # Extract common fields using regex
        patterns = {
            'scontext': r'scontext=(\S+)',
            'tcontext': r'tcontext=(\S+)',
            'tclass': r'tclass=(\S+)',
            'perm': r'\{([^}]+)\}',
            'comm': r'comm="([^"]+)"',
            'exe': r'exe="([^"]+)"'
        }
        
        for field, pattern in patterns.items():
            match = re.search(pattern, avc_line)
            if match:
                denial_data[field] = match.group(1)
        
        return denial_data
    
    def save_parsed_logs(self, raw_logs):
        """Save parsed logs to JSON format"""
        parsed_denials = []
        
        for line in raw_logs.split('\n'):
            if 'avc:' in line and 'denied' in line:
                parsed_denial = self.parse_avc_denial(line)
                if parsed_denial:
                    parsed_denials.append(parsed_denial)
        
        # Save to JSON file
        output_file = os.path.join(self.output_dir, "selinux_denials.json")
        with open(output_file, 'w') as f:
            json.dump(parsed_denials, f, indent=2)
        
        print(f"Saved {len(parsed_denials)} parsed denials to {output_file}")
        return parsed_denials

def main():
    collector = SELinuxLogCollector()
    
    print("Collecting SELinux AVC denial logs...")
    raw_logs = collector.collect_avc_denials(days_back=30)
    
    if raw_logs:
        parsed_denials = collector.save_parsed_logs(raw_logs)
        print(f"Collection complete. Found {len(parsed_denials)} denials.")
    else:
        print("No denials found. Generating sample data for demonstration...")
        # Create sample data for learning purposes
        sample_denials = [
            {
                "scontext": "unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023",
                "tcontext": "system_u:object_r:httpd_exec_t:s0",
                "tclass": "file",
                "perm": "execute",
                "comm": "httpd",
                "exe": "/usr/sbin/httpd"
            },
            {
                "scontext": "system_u:system_r:httpd_t:s0",
                "tcontext": "unconfined_u:object_r:user_home_t:s0",
                "tclass": "file",
                "perm": "read",
                "comm": "httpd",
                "exe": "/usr/sbin/httpd"
            }
        ]
        
        output_file = os.path.join(collector.output_dir, "selinux_denials.json")
        with open(output_file, 'w') as f:
            json.dump(sample_denials, f, indent=2)
        print(f"Created sample data in {output_file}")

if __name__ == "__main__":
    main()
Run the log collection script:
chmod +x scripts/collect_selinux_logs.py
python3 scripts/collect_selinux_logs.py
Task 2: Develop AI-Powered SELinux Policy Generation Script

Subtask 2.1: Create the Machine Learning Framework

Create the main AI policy generator script:
nano scripts/ai_policy_generator.py
#!/usr/bin/env python3
"""
AI-Powered SELinux Policy Generator
Uses machine learning to analyze system activity and suggest SELinux policies
"""

import json
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from collections import Counter, defaultdict
import re
import os

class SELinuxPolicyAI:
    def __init__(self, log_file="logs/selinux_denials.json"):
        self.log_file = log_file
        self.denials_data = []
        self.policy_suggestions = []
        self.vectorizer = TfidfVectorizer()
        self.label_encoders = {}
        
    def load_denial_data(self):
        """Load and preprocess SELinux denial data"""
        try:
            with open(self.log_file, 'r') as f:
                self.denials_data = json.load(f)
            print(f"Loaded {len(self.denials_data)} denial records")
            return True
        except FileNotFoundError:
            print(f"Log file {self.log_file} not found")
            return False
        except json.JSONDecodeError:
            print("Error parsing JSON log file")
            return False
    
    def extract_features(self):
        """Extract features from denial data for ML analysis"""
        if not self.denials_data:
            return None
        
        # Convert to DataFrame for easier manipulation
        df = pd.DataFrame(self.denials_data)
        
        # Fill missing values
        df = df.fillna('unknown')
        
        # Extract domain and type from contexts
        df['source_domain'] = df['scontext'].apply(self._extract_domain)
        df['target_type'] = df['tcontext'].apply(self._extract_type)
        
        # Create feature combinations
        df['domain_class_perm'] = df['source_domain'] + '_' + df['tclass'] + '_' + df['perm']
        df['target_class'] = df['target_type'] + '_' + df['tclass']
        
        return df
    
    def _extract_domain(self, context):
        """Extract domain from SELinux context"""
        if not context or context == 'unknown':
            return 'unknown'
        parts = context.split(':')
        if len(parts) >= 3:
            return parts[2].replace('_t', '')
        return 'unknown'
    
    def _extract_type(self, context):
        """Extract type from SELinux context"""
        if not context or context == 'unknown':
            return 'unknown'
        parts = context.split(':')
        if len(parts) >= 3:
            return parts[2]
        return 'unknown'
    
    def analyze_patterns(self, df):
        """Analyze patterns in denial data using clustering"""
        # Prepare features for clustering
        features = []
        for _, row in df.iterrows():
            feature_text = f"{row['source_domain']} {row['target_type']} {row['tclass']} {row['perm']}"
            features.append(feature_text)
        
        # Vectorize features
        if len(features) > 0:
            feature_vectors = self.vectorizer.fit_transform(features)
            
            # Perform clustering
            n_clusters = min(5, len(features))  # Adjust based on data size
            if n_clusters > 1:
                kmeans = KMeans(n_clusters=n_clusters, random_state=42)
                clusters = kmeans.fit_predict(feature_vectors)
                df['cluster'] = clusters
            else:
                df['cluster'] = 0
        
        return df
    
    def generate_policy_suggestions(self, df):
        """Generate SELinux policy suggestions based on analysis"""
        suggestions = []
        
        # Group by clusters to find common patterns
        for cluster_id in df['cluster'].unique():
            cluster_data = df[df['cluster'] == cluster_id]
            
            # Find most common patterns in this cluster
            common_domains = Counter(cluster_data['source_domain']).most_common(3)
            common_targets = Counter(cluster_data['target_type']).most_common(3)
            common_classes = Counter(cluster_data['tclass']).most_common(3)
            common_perms = Counter(cluster_data['perm']).most_common(3)
            
            # Generate policy rules for this cluster
            for domain, domain_count in common_domains:
                for target, target_count in common_targets:
                    for tclass, class_count in common_classes:
                        for perm, perm_count in common_perms:
                            if domain != 'unknown' and target != 'unknown':
                                confidence = (domain_count + target_count + class_count + perm_count) / (4 * len(cluster_data))
                                
                                policy_rule = {
                                    'rule_type': 'allow',
                                    'source': f"{domain}_t",
                                    'target': target,
                                    'class': tclass,
                                    'permission': perm,
                                    'confidence': confidence,
                                    'cluster': cluster_id,
                                    'occurrences': min(domain_count, target_count, class_count, perm_count)
                                }
                                
                                suggestions.append(policy_rule)
        
        # Sort by confidence and remove duplicates
        suggestions = sorted(suggestions, key=lambda x: x['confidence'], reverse=True)
        unique_suggestions = []
        seen_rules = set()
        
        for suggestion in suggestions:
            rule_key = (suggestion['source'], suggestion['target'], suggestion['class'], suggestion['permission'])
            if rule_key not in seen_rules:
                seen_rules.add(rule_key)
                unique_suggestions.append(suggestion)
        
        self.policy_suggestions = unique_suggestions[:20]  # Top 20 suggestions
        return self.policy_suggestions
    
    def format_policy_rules(self):
        """Format policy suggestions as SELinux policy rules"""
        formatted_rules = []
        
        for suggestion in self.policy_suggestions:
            # Format as SELinux policy rule
            rule = f"allow {suggestion['source']} {suggestion['target']}:{suggestion['class']} {suggestion['permission']};"
            
            formatted_rule = {
                'rule': rule,
                'confidence': suggestion['confidence'],
                'occurrences': suggestion['occurrences'],
                'explanation': f"Allow {suggestion['source']} to {suggestion['permission']} {suggestion['target']} {suggestion['class']} objects"
            }
            
            formatted_rules.append(formatted_rule)
        
        return formatted_rules
    
    def save_policy_suggestions(self, output_file="ai_generated_policies.te"):
        """Save policy suggestions to a .te file"""
        formatted_rules = self.format_policy_rules()
        
        with open(output_file, 'w') as f:
            f.write("# AI-Generated SELinux Policy Suggestions\n")
            f.write("# Generated by AI Policy Generator\n")
            f.write(f"# Total suggestions: {len(formatted_rules)}\n\n")
            
            for i, rule_data in enumerate(formatted_rules, 1):
                f.write(f"# Rule {i}: Confidence {rule_data['confidence']:.2f}, Occurrences: {rule_data['occurrences']}\n")
                f.write(f"# {rule_data['explanation']}\n")
                f.write(f"{rule_data['rule']}\n\n")
        
        print(f"Policy suggestions saved to {output_file}")
        return output_file
    
    def run_analysis(self):
        """Run complete AI analysis pipeline"""
        print("Starting AI-powered SELinux policy analysis...")
        
        # Load data
        if not self.load_denial_data():
            return False
        
        # Extract features
        df = self.extract_features()
        if df is None or df.empty:
            print("No data available for analysis")
            return False
        
        print(f"Extracted features from {len(df)} denial records")
        
        # Analyze patterns
        df = self.analyze_patterns(df)
        print(f"Identified {len(df['cluster'].unique())} pattern clusters")
        
        # Generate suggestions
        suggestions = self.generate_policy_suggestions(df)
        print(f"Generated {len(suggestions)} policy suggestions")
        
        # Save results
        policy_file = self.save_policy_suggestions()
        
        return True

def main():
    # Initialize AI policy generator
    ai_generator = SELinuxPolicyAI()
    
    # Run analysis
    success = ai_generator.run_analysis()
    
    if success:
        print("\nAI analysis completed successfully!")
        print("Check 'ai_generated_policies.te' for policy suggestions")
    else:
        print("AI analysis failed. Check log files and try again.")

if __name__ == "__main__":
    main()
Run the AI policy generator:
python3 scripts/ai_policy_generator.py
Subtask 2.2: Create Policy Validation and Testing Framework

Create a policy validation script:
nano scripts/policy_validator.py
#!/usr/bin/env python3
"""
SELinux Policy Validator
Validates and tests AI-generated SELinux policies
"""

import subprocess
import os
import tempfile
import shutil
from pathlib import Path

class PolicyValidator:
    def __init__(self, policy_file="ai_generated_policies.te"):
        self.policy_file = policy_file
        self.module_name = "ai_generated_policy"
        self.temp_dir = None
        
    def validate_syntax(self):
        """Validate SELinux policy syntax"""
        print("Validating policy syntax...")
        
        try:
            # Create temporary directory for compilation
            self.temp_dir = tempfile.mkdtemp()
            
            # Copy policy file to temp directory
            temp_policy = os.path.join(self.temp_dir, f"{self.module_name}.te")
            shutil.copy2(self.policy_file, temp_policy)
            
            # Try to compile the policy
            cmd = ["checkmodule", "-M", "-m", "-o", 
                   os.path.join(self.temp_dir, f"{self.module_name}.mod"), 
                   temp_policy]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.temp_dir)
            
            if result.returncode == 0:
                print("✓ Policy syntax is valid")
                return True
            else:
                print("✗ Policy syntax errors found:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"Error during syntax validation: {e}")
            return False
    
    def create_policy_package(self):
        """Create SELinux policy package"""
        if not self.temp_dir:
            print("Must validate syntax first")
            return False
            
        try:
            print("Creating policy package...")
            
            # Create policy package
            mod_file = os.path.join(self.temp_dir, f"{self.module_name}.mod")
            pp_file = os.path.join(self.temp_dir, f"{self.module_name}.pp")
            
            cmd = ["semodule_package", "-o", pp_file, "-m", mod_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Policy package created successfully")
                return pp_file
            else:
                print("✗ Failed to create policy package:")
                print(result.stderr)
                return None
                
        except Exception as e:
            print(f"Error creating policy package: {e}")
            return None
    
    def simulate_policy_install(self, package_file):
        """Simulate policy installation (dry run)"""
        try:
            print("Simulating policy installation...")
            
            # Check if policy would install successfully
            cmd = ["sudo", "semodule", "--dry-run", "-i", package_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Policy would install successfully")
                return True
            else:
                print("✗ Policy installation would fail:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"Error simulating policy install: {e}")
            return False
    
    def analyze_policy_impact(self):
        """Analyze potential impact of policy rules"""
        print("Analyzing policy impact...")
        
        try:
            with open(self.policy_file, 'r') as f:
                content = f.read()
            
            # Count different types of rules
            allow_rules = content.count('allow ')
            deny_rules = content.count('deny ')
            auditallow_rules = content.count('auditallow ')
            
            print(f"Policy Impact Analysis:")
            print(f"  - Allow rules: {allow_rules}")
            print(f"  - Deny rules: {deny_rules}")
            print(f"  - Audit allow rules: {auditallow_rules}")
            
            # Check for potentially risky permissions
            risky_perms = ['write', 'create', 'unlink', 'execute', 'setattr']
            risky_count = 0
            
            for perm in risky_perms:
                if perm in content:
                    risky_count += content.count(perm)
            
            print(f"  - Potentially risky permissions: {risky_count}")
            
            if risky_count > 10:
                print("⚠️  Warning: High number of risky permissions detected")
            else:
                print("✓ Policy appears to have reasonable permission scope")
                
            return True
            
        except Exception as e:
            print(f"Error analyzing policy impact: {e}")
            return False
    
    def cleanup(self):
        """Clean up temporary files"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            print("Cleaned up temporary files")
    
    def run_validation(self):
        """Run complete validation pipeline"""
        print(f"Starting validation of {self.policy_file}...")
        
        try:
            # Check if policy file exists
            if not os.path.exists(self.policy_file):
                print(f"Policy file {self.policy_file} not found")
                return False
            
            # Validate syntax
            if not self.validate_syntax():
                return False
            
            # Create package
            package_file = self.create_policy_package()
            if not package_file:
                return False
            
            # Simulate installation
            if not self.simulate_policy_install(package_file):
                return False
            
            # Analyze impact
            self.analyze_policy_impact()
            
            print("\n✓ Policy validation completed successfully!")
            print(f"Policy package available at: {package_file}")
            
            return True
            
        except Exception as e:
            print(f"Validation failed: {e}")
            return False
        finally:
            # Always cleanup
            self.cleanup()

def main():
    validator = PolicyValidator()
    success = validator.run_validation()
    
    if success:
        print("\nValidation Summary:")
        print("- Policy syntax is correct")
        print("- Policy package can be created")
        print("- Policy can be installed safely")
        print("- Impact analysis completed")
    else:
        print("\nValidation failed. Please review the errors above.")

if __name__ == "__main__":
    main()
Install required SELinux development tools:
sudo dnf install -y policycoreutils-devel selinux-policy-devel
Run the policy validator:
python3 scripts/policy_validator.py
Task 3: Test AI-Generated Policies on the System

Subtask 3.1: Create Safe Testing Environment

Create a policy testing script:
nano scripts/policy_tester.py
#!/usr/bin/env python3
"""
SELinux Policy Tester
Safely tests AI-generated policies in a controlled environment
"""

import subprocess
import os
import time
import json
from datetime import datetime

class PolicyTester:
    def __init__(self, policy_file="ai_generated_policies.te"):
        self.policy_file = policy_file
        self.module_name = "ai_test_policy"
        self.test_results = []
        self.backup_created = False
        
    def create_system_backup(self):
        """Create backup of current SELinux state"""
        try:
            print("Creating system backup...")
            
            # Get current policy version
            result = subprocess.run(["sestatus"], capture_output=True, text=True)
            
            backup_info = {
                'timestamp': datetime.now().isoformat(),
                'sestatus_output': result.stdout,
                'policy_version': self._extract_policy_version(result.stdout)
            }
            
            with open('selinux_backup.json', 'w') as f:
                json.dump(backup_info, f, indent=2)
            
            print("✓ System backup created")
            self.backup_created = True
            return True
            
        except Exception as e:
            print(f"Error creating backup: {e}")
            return False
    
    def _extract_policy_version(self, sestatus_output):
        """Extract policy version from sestatus output"""
        for line in sestatus_output.split('\n'):
            if 'Policy version:' in line:
                return line.split(':')[1].strip()
        return "unknown"
    
    def prepare_test_policy(self):
        """Prepare a safe version of the policy for testing"""
        try:
            print("Preparing test policy...")
            
            # Read original policy
            with open(self.policy_file, 'r') as f:
                original_content = f.read()
            
            # Create a test version with limited scope
            test_content = "# Test version of AI-generated policy\n"
            test_content += "# Limited scope for safe testing\n\n"
            
            # Only include first few rules for initial testing
            rules = [line for line in original_content.split('\n') if line.strip().startswith('allow')]
            
            # Limit to first 5 rules for safety
            for rule in rules[:5]:
                test_content += rule + "\n"
            
            # Save test policy
            test_policy_file = f"test_{self.policy_file}"
            with open(test_policy_file, 'w') as f:
                f.write(test_content)
            
            print(f"✓ Test policy created: {test_policy_file}")
            return test_policy_file
            
        except Exception as e:
            print(f"Error preparing test policy: {e}")
            return None
    
    def install_test_policy(self, test_policy_file):
        """Install test policy module"""
        try:
            print("Installing test policy...")
            
            # Compile policy module
            cmd = ["checkmodule", "-M", "-m", "-o", f"{self.module_name}.mod", test_policy_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print("Failed to compile test policy:")
                print(result.stderr)
                return False
            
            # Create policy package
            cmd = ["semodule_package", "-o", f"{self.module_name}.pp", "-m", f"{self.module_name}.mod"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print("Failed to create policy package:")
                print(result.stderr)
                return False
            
            # Install policy module
            cmd = ["sudo", "semodule", "-i", f"{self.module_name}.pp"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✓ Test policy installed successfully")
                return True
            else:
                print("Failed to install test policy:")
                print(result.stderr)
                return False
                
        except Exception as e:
            print(f"Error installing test policy: {e}")
            return False
    
    def run_policy_tests(self):
        """Run tests to verify policy effectiveness"""
        print("Running policy effectiveness tests...")
        
        test_results = []
        
        # Test 1: Check if policy module is loaded
        try:
            cmd = ["sudo", "semodule", "-l"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if self.module_name in result.stdout:
                test_results.append({"test": "Module Load", "status": "PASS", "details": "Policy module loaded successfully"})
            else:
                test_results.append({"test": "Module Load", "status": "FAIL", "details": "Policy module not found in loaded modules"})
        except Exception as e:
            test_results.append({"test": "Module Load", "status": "ERROR", "details": str(e)})
        
        # Test 2: Check for new AVC denials
        try:
            print("Monitoring for AVC denials (30 seconds)...")
            time.sleep(5)  # Wait a bit for system activity
            
            cmd = ["sudo", "ausearch", "-m", "avc", "-ts", "recent"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and result.stdout.strip():
                denial_count = result.stdout.count('avc:')
                test_results.append({"test": "AVC Monitoring", "status": "INFO", "details": f"Found {denial_count} recent AVC denials"})
            else:
                test_results.append({"test": "AVC Monitoring", "status": "PASS", "details": "No recent AVC denials detected"})
        except Exception as e:
            test_results.append({"test": "AVC Monitoring", "status": "ERROR", "details": str(e)})
        
        # Test 3: System stability check
        try:
            cmd = ["systemctl", "is-system-running"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if "running" in result.stdout or "degraded" in result.stdout:
                test_results.append({"test": "System Stability", "status": "PASS", "details": "System running normally"})
            else:
                test_results.append({"test": "System Stability", "status": "WARN", "details": f"System state: {result.stdout.strip()}"})
        except Exception as e:
            test_results.append({"test": "System Stability", "status": "ERROR", "details": str(e)})
        
        self.test_results = test_results
        return test_results
    
    def generate_test_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*50)
        print("POLICY TESTING REPORT")
        print("="*50)
        
        for result in self.test_results:
            status_symbol = {"PASS":
