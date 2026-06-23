"""Seyahat Geçmişi Yönetimi

Kullanıcı tarafından planlanan rotaların tarihçesini JSON dosyasına kaydeder ve yükler.
"""

import json
from datetime import datetime
from pathlib import Path

from config import DATA_DIR

FILE_PATH = DATA_DIR / "trips_history.json"


def save_trip(trip):
    """Seyahat kaydını dosyaya kaydeder.

    Args:
        trip: Kaydedilecek seyahat nesnesi veya sözlüğü.
    """
    try:
        with open(FILE_PATH, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    record = {
        "from": (
            trip.get("from")
            if isinstance(trip, dict)
            else (trip.steps[0].from_stop_id if trip.steps else None)
        ),
        "to": (
            trip.get("to")
            if isinstance(trip, dict)
            else (trip.steps[-1].to_stop_id if trip.steps else None)
        ),
        "duration": (
            trip.get("total_duration_min")
            if isinstance(trip, dict)
            else trip.total_duration_min
        ),
        "fare": trip.get("total_fare") if isinstance(trip, dict) else trip.total_fare,
        "timestamp": str(datetime.now()),
    }

    data.append(record)

    try:
        with open(FILE_PATH, "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"[!] Seyahat kaydedilemedi: {e}")


def load_trips():
    """Kaydedilmiş seyahatleri dosyadan yükler.

    Returns:
        Seyahat kayıtlarının listesi.
    """
    try:
        with open(FILE_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_all_trips(trips):
    """Tüm seyahat kayıtlarını dosyaya kaydeder (tüm veriyi değiştirir).

    Args:
        trips: Seyahat kayıtlarının listesi.
    """
    if not isinstance(trips, list):
        return

    try:
        with open(FILE_PATH, "w") as f:
            json.dump(trips, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"[!] Seyahatler kaydedilemedi: {e}")
