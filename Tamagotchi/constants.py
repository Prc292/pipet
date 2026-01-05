import os

# --- GLOBAL CONFIGURATION ---
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 320
FPS = 30


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_FILE = os.path.join(DATA_DIR, "pet_life.db")

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