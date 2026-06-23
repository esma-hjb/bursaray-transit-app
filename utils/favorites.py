"""Kullanıcı Favori Durakları Yönetimi

Kullanıcının favorilerine eklediği durakları JSON dosyasında saklar ve yükler.
"""

import json
from config import DATA_DIR

FILE = DATA_DIR / "favorites.json"


def load_favorites():
    """Favori durakları dosyadan yükler."""
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_favorite(stop_id):
    """Favori durak listesine yeni durak ekler."""
    if not stop_id or not isinstance(stop_id, str):
        return

    favs = load_favorites()
    if stop_id not in favs:
        favs.append(stop_id)

    try:
        with open(FILE, "w", encoding="utf-8") as f:
            json.dump(favs, f, indent=4, ensure_ascii=False)
    except IOError as e:
        print(f"[!] Favori kaydedilemedi: {e}")
