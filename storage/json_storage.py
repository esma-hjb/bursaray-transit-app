"""JSON kalıcılık katmanı."""

from __future__ import annotations

import json
from pathlib import Path

from utils.exceptions import StorageError


def read_json(path, default=None):
    """Bir JSON dosyasını okur. Dosya yoksa veya boşsa 'default' döndürür."""
    p = Path(path)
    if not p.exists():
        return default
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        return default
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise StorageError(f"JSON okunamadı ({path}): {e}") from e


def write_json(path, data):
    """Veriyi JSON dosyasına yazar. Klasör yoksa oluşturur."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    try:
        with p.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except OSError as e:
        raise StorageError(f"JSON yazılamadı ({path}): {e}") from e
