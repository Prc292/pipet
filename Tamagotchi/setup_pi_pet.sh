#!/bin/bash

# --- Full setup script for Pocket Pi Pet on Raspberry Pi OS Lite ---
set -e

REPO_URL="https://github.com/Prc292/pocket-pi-pet.git"
CLONE_DIR="pocket-pi-pet"
VENV_DIR="$HOME/tamago-venv"

echo "--- STARTING AUTOMATED SETUP for $CLONE_DIR ---"

# 1. Update system
echo "1. Updating system..."
sudo apt update
sudo apt upgrade -y

# 2. Install required system libraries and SDL2 runtime/development packages
echo "2. Installing required system libraries..."
sudo apt install -y python3 python3-pip python3-venv python3-dev python3-setuptools \
    libsdl2-2.0-0 libsdl2-dev libsdl2-image-2.0-0 libsdl2-mixer-2.0-0 libsdl2-ttf-2.0-0 \
    libdrm-dev libgbm-dev libmtdev-dev libudev-dev libevdev-dev \
    libegl-mesa0 libgles2-mesa0 mesa-utils mesa-utils-extra \
    libjpeg62-turbo libpng16-16 libportmidi0 git sqlite3

# 3. Create Python virtual environment
echo "3. Creating Python virtual environment..."
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install pygame

# 4. Clone or update the repository
echo "4. Cloning or updating the repository..."
cd ~
if [ -d "$CLONE_DIR" ]; then
    echo "Directory '$CLONE_DIR' exists, pulling latest changes..."
    cd "$CLONE_DIR"
    git pull origin main
else
    git clone "$REPO_URL"
    cd "$CLONE_DIR"
fi

# 5. Set executable permissions
echo "5. Setting executable permissions for main.py..."
cd ~/pocket-pi-pet/Tamagotchi
chmod +x main.py

echo "--- SETUP COMPLETE ---"
echo "The game is installed in: ~/pocket-pi-pet"
echo ""
echo "TO RUN THE GAME:"
echo "  source ~/tamago-venv/bin/activate"
echo "  python3 ~/pocket-pi-pet/Tamagotchi/main.py"
