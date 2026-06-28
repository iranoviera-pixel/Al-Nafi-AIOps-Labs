Lab 73: Signing Container Images

Objectives

By the end of this lab, you will be able to:

Understand the tools required for container image signing.
Sign a container image using podman.
Verify the authenticity of a signed image.
Automate the signing and verification process using a script.
Prerequisites

Before starting this lab, ensure you have:

Basic familiarity with Linux command line.
A running Linux-based cloud machine (provided by Al Nafi—click Start Lab to launch).
podman installed (pre-configured in Al Nafi's lab environment).
Task 1: Install Necessary Tools for Image Signing

Subtask 1.1: Verify Podman Installation

Run the following command to check if podman is installed:

podman --version
Expected Output:
podman version 4.x.x (or similar)

Subtask 1.2: Install GPG (GNU Privacy Guard)

GPG is required for generating cryptographic keys. Install it using:

sudo apt-get update && sudo apt-get install -y gnupg
Verification:
Run gpg --version to confirm installation.

Task 2: Sign a Container Image Using Podman

Subtask 2.1: Generate a GPG Key Pair

Generate a new GPG key:

gpg --full-generate-key
Select RSA and RSA as the key type.
Use 2048 bits for key size.
Set an expiration date (e.g., 30d for 30 days).
Enter your name and email (use lab credentials if prompted).
List your keys to verify:

gpg --list-secret-keys
Expected Output:
A list of your GPG keys with IDs (e.g., ABC12345).

Subtask 2.2: Pull a Test Image

Pull a lightweight image (e.g., alpine) to sign:

podman pull alpine:latest
Subtask 2.3: Sign the Image

Sign the image using your GPG key:

podman image sign --sign-by your-email@example.com alpine:latest
Replace your-email@example.com with the email used in Subtask 2.1.

Expected Outcome:
The image is signed, and a signature is stored locally.

Task 3: Verify the Image Signature

Subtask 3.1: Export the Public Key

Export your public key to verify the signature:

gpg --export --armor your-email@example.com > public-key.gpg
Subtask 3.2: Verify the Signature

Verify the signed image:

podman image trust show alpine:latest
Expected Output:
A message confirming the signature is valid.

Task 4: Automate Signing and Verification with a Script

Subtask 4.1: Create a Signing Script

Create a script named sign_and_verify.sh:

#!/bin/bash
# Sign and verify a container image

IMAGE="alpine:latest"
GPG_EMAIL="your-email@example.com"

# Sign the image
podman image sign --sign-by $GPG_EMAIL $IMAGE

# Verify the signature
podman image trust show $IMAGE
Subtask 4.2: Make the Script Executable

chmod +x sign_and_verify.sh
Subtask 4.3: Run the Script

./sign_and_verify.sh
Expected Outcome:
The script signs the image and outputs verification details.
