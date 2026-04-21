# Lab 20: Compiling Apache HTTP Server from Source

Laboratorium ini mendemonstrasikan proses mengunduh, mengonfigurasi, dan mengompilasi perangkat lunak Apache (httpd) langsung dari kode sumber di sistem operasi CentOS.

## Prasyarat (Dependencies)
Sebelum melakukan kompilasi, sistem memerlukan alat pengembangan (build tools) dan library pendukung. Karena menggunakan CentOS, kita menggunakan `yum`:

```bash
# Update repositori dan install tools dasar
sudo yum update -y
sudo yum install -y wget tar gcc make

# Install library pendukung untuk Apache (Penting agar tidak error APR)
sudo yum install -y apr-devel apr-util-devel pcre-devel
