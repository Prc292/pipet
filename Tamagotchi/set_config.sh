

#!/bin/bash
# Pocket Pi Pet - config.txt KMS/OpenGL setup script
# This script enables KMS OpenGL and framebuffer support for Pygame on Raspberry Pi OS Lite

set -e

CONFIG_FILE="/boot/firmware/config.txt"
BACKUP_FILE="/boot/firmware/config.txt.bak"

echo "Backing up original config.txt..."
sudo cp "$CONFIG_FILE" "$BACKUP_FILE"

echo "Adding KMS/OpenGL settings to config.txt..."
# Remove existing dtoverlay=vc4-kms-v3d line if present
sudo sed -i '/^dtoverlay=vc4-kms-v3d/d' "$CONFIG_FILE"
# Remove existing max_framebuffers line if present
sudo sed -i '/^max_framebuffers=/d' "$CONFIG_FILE"

# Append new settings
echo "dtoverlay=vc4-kms-v3d" | sudo tee -a "$CONFIG_FILE"
echo "max_framebuffers=2" | sudo tee -a "$CONFIG_FILE"

echo "config.txt updated. Backup saved as config.txt.bak"
echo "Please reboot your Pi for changes to take effect:"
echo "  sudo reboot"