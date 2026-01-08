#!/bin/bash
# setup_tamagotchi.sh
# One-shot installer for PetPi / Tamagotchi game
# Designed for Raspberry Pi OS Bookworm Lite + USB touchscreen

set -e  # exit on errors

cd ~

# 1️⃣ Clone repo into ~/pipet
if [ ! -d "pipet" ]; then
    echo "Cloning repo into ~/pipet..."
    git clone -b dev https://github.com/YOUR_USERNAME/YOUR_REPO.git pipet
else
    echo "~/pipet already exists — updating..."
    cd pipet
    git pull
    cd ..
fi

# 2️⃣ Install system dependencies
echo "Installing required system packages..."
sudo apt update
sudo apt install -y \
    git \
    python3 python3-pip python3-venv \
    libsdl2-2.0-0 \
    libsdl2-image-2.0-0 \
    libsdl2-mixer-2.0-0 \
    libsdl2-ttf-2.0-0 \
    python3-pygame \
    libts0 libts-bin \
    pulseaudio pulseaudio-utils libasound2-plugins \
    libgles2-mesa-dev libegl1-mesa-dev mesa-utils libgl-dev libegl-dev libgles-dev

# 3️⃣ Create Python virtual environment in ~/pipet/venv
if [ ! -d "~/pipet/venv" ]; then
    echo "Creating Python virtual environment in ~/pipet/venv..."
    python3 -m venv ~/pipet/venv
fi

source ~/pipet/venv/bin/activate

# 4️⃣ Python dependencies
echo "Upgrading pip..."
pip install --upgrade pip

if [ -f ~/pipet/Tamagotchi/requirements.txt ]; then
    echo "Installing Python dependencies from requirements.txt..."
    pip install -r ~/pipet/Tamagotchi/requirements.txt
else
    pip install pygame
fi

# 5️⃣ Start PulseAudio
echo "Starting PulseAudio..."
pulseaudio --start || true

# 6️⃣ Update /boot/firmware/config.txt with HDMI/KMS settings
echo "Configuring /boot/firmware/config.txt for HDMI/KMS..."
CONFIG_BLOCK="
dtoverlay=vc4-kms-v3d
max_framebuffers=2
disable_fw_kms_setup=1
arm_boost=1
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=2
hdmi_cvt=1280 720 30 6 0 0 0
"

if ! grep -q "dtoverlay=vc4-kms-v3d" /boot/firmware/config.txt; then
    echo "$CONFIG_BLOCK" | sudo tee -a /boot/firmware/config.txt > /dev/null
    echo "Added HDMI/touchscreen KMS settings to config.txt"
else
    echo "config.txt already has these settings — skipping"
fi

# 7️⃣ Set environment variables for Pygame/Tamagochi
export SDL_VIDEODRIVER=KMSDRM
export SDL_FBDEV=/dev/fb0
export SDL_MOUSEDRV=TSLIB
export SDL_MOUSEDEV=/dev/input/event0
export SDL_AUDIODRIVER=pulse

echo ""
echo "======================================================"
echo "INSTALL COMPLETE!"
echo "Reboot required for config.txt changes and EGL/OpenGL to take effect."
echo ""
echo "To run the game after reboot:"
echo "  source ~/pipet/venv/bin/activate"
echo "  python3 ~/pipet/Tamagotchi/main.py"
echo "======================================================"

# Optional: Uncomment the next line if you want the script to reboot automatically
echo "Rebooting in 5 seconds..."
sleep 5
sudo reboot