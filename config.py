"""Uygulama genel ayarları ve sabitleri."""
from pathlib import Path

# --- Yollar ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STOPS_FILE = DATA_DIR / "stops.json"
ROUTES_FILE = DATA_DIR / "routes.json"
SCHEDULE_FILE = DATA_DIR / "schedule.json"
USER_DATA_FILE = DATA_DIR / "user_data.json"

# --- Dış API (Faz 4) ---
API_BASE_URL = "https://example-bursa-transit-api/v1"
API_TIMEOUT = 10
API_MAX_RETRIES = 3

# --- Yakın durak (Faz 5) ---
NEARBY_RADIUS_M = 500
NEARBY_RADIUS_EXPANDED_M = 1500

# --- Canlı takip (Faz 6) ---
ETA_REFRESH_SECONDS = 10

# --- Kullanıcı tercihleri ---
DEFAULT_LANGUAGE = "tr"
SUPPORTED_LANGUAGES = ["tr", "en"]