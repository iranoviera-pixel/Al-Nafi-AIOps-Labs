#!/bin/bash

# --- Variabel Data Anda ---
REMOTE_USER="noviera"
REMOTE_HOST="192.168.64.2"
SOURCE_DIR="testdir/"
DEST_DIR="/home/noviera/"
# Simpan log di folder saat ini agar tidak error permission
LOG_FILE="./file_transfer.log"

# --- Fungsi Log ---
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# --- Proses Utama ---
log "Starting file transfer to $REMOTE_HOST"
echo "Memulai transfer... pantau log di $LOG_FILE"

# Menggunakan rsync dengan progress
rsync -avz --progress testdir/ $REMOTE_USER@$REMOTE_HOST:$DEST_DIR >> "$LOG_FILE" 2>&1

# Mengecek apakah rsync sukses
if [ $? -eq 0 ]; then
    log "Transfer completed successfully"
    echo "Berhasil! Cek file_transfer.log"
else
    log "Transfer failed"
    echo "Gagal! Periksa file_transfer.log untuk detailnya"
    exit 1
fi


