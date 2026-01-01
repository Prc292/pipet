#!/usr/bin/env bash
set -euo pipefail

# Minimal Pi OS Lite setup for Pocket Pi-Pet
# Run as root or with sudo: sudo ./pi_install_deps.sh <user>
USER_NAME=${1:-pi}
PROJECT_DIR=${2:-/home/$USER_NAME/pocket-pi-pet}

echo "Updating packages and installing system dependencies..."
apt update
apt install -y python3 python3-venv python3-dev build-essential \
  libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libasound2-dev \
  libjpeg-dev libpng-dev libportmidi-dev

echo "Creating virtualenv and installing Python packages..."
python3 -m venv "$PROJECT_DIR/.venv"
. "$PROJECT_DIR/.venv/bin/activate"
python -m pip install --upgrade pip
pip install -r "$PROJECT_DIR/requirements.txt"

echo "Adding $USER_NAME to video and input groups (may be required for DRM/framebuffer and input devices)"
usermod -aG video,input "$USER_NAME" || true

cat <<'EOF'
Done. Next steps:
- Ensure your project is located at $PROJECT_DIR (or adjust paths in the systemd unit).
- Mark the script executable: chmod +x scripts/pi_install_deps.sh
- Consider installing the included systemd unit file to /etc/systemd/system/tamagotchi.service and running:
    sudo systemctl daemon-reload
    sudo systemctl enable tamagotchi.service
    sudo systemctl start tamagotchi.service
EOF