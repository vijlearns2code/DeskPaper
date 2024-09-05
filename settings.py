import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

API_KEY = os.getenv("API_KEY", '4902c96f354b427b81f143025240707')
CITY = os.getenv("CITY", 'Pondicherry')
CurrentUrl = "http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={CITY}&aqi=no"
CURRENT_THEME = "default"

# true for no APIs
OFFLINE = False

PIC_URL = "https://www.theweather.com/wimages/foto02f2e4a60a94f4e9ace5703c94b02735.png"
# Check if the OS is Windows
ISWINDOWS = (os.name == 'nt')

# Define directory paths
BASE_DIR = Path(__file__).parent.parent
ASSETS_DIR = BASE_DIR / 'assets'
GENERATED_DIR = BASE_DIR / 'generated'
DEBUG_DIR = BASE_DIR / 'debug'

# Define file paths for templates and wallpapers
TEMPLATE = GENERATED_DIR / 'template.jpeg'
DOWNLOAD = GENERATED_DIR / 'download.jpeg'
OK_WALLPAPER = GENERATED_DIR / 'wallpaper.jpeg'
ERROR_WALLPAPER = GENERATED_DIR / 'error.jpeg'
ERROR_BG = GENERATED_DIR / 'error.jpeg'
