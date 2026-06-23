"""Uygulama genel ayarları ve sabitleri."""

from pathlib import Path

# --- Yollar ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STOPS_FILE = DATA_DIR / "stops.json"
ROUTES_FILE = DATA_DIR / "routes.json"
SCHEDULE_FILE = DATA_DIR / "schedule.json"
USER_DATA_FILE = DATA_DIR / "user_data.json"

# --- Dış API ---
# Geliştirme sırasında yerel mock API sunucusu kullanılır.
# API çalışmıyorsa LiveBusService otomatik mock veriye geçer.
API_BASE_URL = "http://127.0.0.1:5000"
API_TIMEOUT = 3  # Hızlı timeout — mock'a hızlı düşsün

# --- Yakın durak ---
NEARBY_RADIUS_M = 500
NEARBY_RADIUS_EXPANDED_M = 1500

# --- Kullanıcı tercihleri ---
DEFAULT_LANGUAGE = "tr"
SUPPORTED_LANGUAGES = ["tr", "en"]
