import os

# --- GLOBAL CONFIGURATION ---
SCREEN_WIDTH = 480          
SCREEN_HEIGHT = 320
FPS = 30
DB_FILE = "pet_life.db"
TIME_SCALE_FACTOR = 1 # 1 = real time, 10 = 10x faster!
POINTS_PER_WIN = 10

# Base directory for assets, relative to this file's location
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_PATH = os.path.join(BASE_DIR, "assets")

# --- SHOP (Prices in Coins) ---
SHOP_ITEMS = [
    {'id': 'placeholder_food', 'name': 'Placeholder Food', 'price': 10, 'hunger': 20, 'energy': 5, 'happiness': 5, 'description': 'A generic food item.'},
    {'id': 'placeholder_toy', 'name': 'Placeholder Toy', 'price': 20, 'happiness': 15, 'discipline': 5, 'description': 'A generic toy item.'},
]

# Removed CATEGORIES as they are no longer used.

# --- RETRO UI PALETTE ---
COLOR_BG = (40, 44, 52)
COLOR_PET_BODY = (171, 220, 255)
COLOR_PET_EYES = (33, 37, 43)
COLOR_UI_BAR_BG = (62, 68, 81)
COLOR_HEALTH = (152, 195, 121)
COLOR_FULLNESS = (224, 108, 117)
COLOR_HAPPY = (229, 192, 123)
COLOR_ENERGY = (97, 175, 239)
COLOR_TEXT = (171, 178, 191)
COLOR_BTN = (100, 100, 100)
COLOR_SICK = (198, 120, 221)
COLOR_MESSAGE_BOX_BG = (50, 50, 50, 128) # Semi-transparent dark grey

# --- COMMON COLORS ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (100, 100, 100)
PINK = (255, 182, 193)
ORANGE = (255, 165, 0)
BLUE = (100, 149, 237)
YELLOW = (255, 215, 0)