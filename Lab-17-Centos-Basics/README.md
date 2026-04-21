Subtask 1.2: Install a Package with RPM

RPM requires manual dependency resolution but is useful for local .rpm files.

Download an RPM package (e.g., example.rpm):

wget https://example.com/example.rpm
Install the RPM package:

sudo rpm -ivh example.rpm
Flags:
-i: Install.
-v: Verbose output.
-h: Show progress bar.
Expected Outcome: The package is installed if dependencies are met.
Troubleshooting: If dependencies are missing, use yum install to resolve them.

Verify installation:

rpm -q example
Expected Outcome: The package name and version are displayed.


