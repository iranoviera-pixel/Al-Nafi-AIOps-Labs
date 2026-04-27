#!/bin/bash

# Usage: sudo ./add_mount.sh /dev/sda2 /mnt/data ext4

DEVICE=$1
MOUNT_POINT=$2
FS_TYPE=$3

# 1. Validasi input
if [ -z "$DEVICE" ] || [ -z "$MOUNT_POINT" ] || [ -z "$FS_TYPE" ]; then
    echo "Usage: sudo $0 <device> <mount_point> <filesystem_type>"
    exit 1
fi

# 2. Ambil UUID dan pastikan perangkat ada
UUID=$(sudo blkid -s UUID -o value "$DEVICE")

if [ -z "$UUID" ]; then
    echo "Error: UUID tidak ditemukan untuk $DEVICE. Pastikan disk sudah diformat."
    exit 1
fi

# 3. Buat mount point jika belum ada
if [ ! -d "$MOUNT_POINT" ]; then
    sudo mkdir -p "$MOUNT_POINT"
fi

# 4. Cek apakah UUID sudah ada di /etc/fstab agar tidak duplikat
if grep -q "$UUID" /etc/fstab; then
    echo "Info: UUID $UUID sudah terdaftar di /etc/fstab. Melewati langkah penulisan."
else
    echo "Adding entry to /etc/fstab..."
    echo "UUID=$UUID $MOUNT_POINT $FS_TYPE defaults 0 2" | sudo tee -a /etc/fstab
fi

# 5. Reload systemd (penting untuk distro modern)
sudo systemctl daemon-reload

# 6. Mount semua dan verifikasi
sudo mount -a
if mountpoint -q "$MOUNT_POINT"; then
    echo "Berhasil! $DEVICE terpasang di $MOUNT_POINT."
else
    echo "Gagal melakukan mount. Periksa kembali konfigurasi /etc/fstab."
fi


