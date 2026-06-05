
---

## 0.4 — `config.py`
**Neden:** Sabit değerleri (dosya yolları, API adresi, yarıçaplar, ETA aralığı) tek bir yerde toplar. Kod içine "sihirli sayı" yazmak yerine buradan okunur; değiştirmesi kolay olur.

**İçine yaz:**
```python
"""Uygulama genel ayarlari ve sabitleri."""
from pathlib import Path

# --- Yollar ---
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
STOPS_FILE = DATA_DIR / "stops.json"
ROUTES_FILE = DATA_DIR / "routes.json"
SCHEDULE_FILE = DATA_DIR / "schedule.json"
USER_DATA_FILE = DATA_DIR / "user_data.json"   # runtime'da üretilir

# --- Dış API (Faz 4) ---
API_BASE_URL = "https://example-bursa-transit-api/v1"   # gerçek adresle değiştir
API_TIMEOUT = 10        # saniye
API_MAX_RETRIES = 3     # flowchart: "Retry x3"

# --- Yakın durak (Faz 5) ---
NEARBY_RADIUS_M = 500       # flowchart: 500m
NEARBY_RADIUS_EXPANDED_M = 1500   # flowchart: boşsa 1500m'e genişlet

# --- Canlı takip (Faz 6) ---
ETA_REFRESH_SECONDS = 10    # flowchart: her 10 saniyede güncelle

# --- Kullanıcı tercihleri ---
DEFAULT_LANGUAGE = "tr"
SUPPORTED_LANGUAGES = ["tr", "en"]