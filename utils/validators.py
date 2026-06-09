"""Girdi dogrulama yardimcilari."""
from __future__ import annotations

from config import SUPPORTED_LANGUAGES


def validate_language(lang: str) -> str:
    """Dil kodunu dogrular; gecersizse ValueError firlatir."""
    if lang not in SUPPORTED_LANGUAGES:
        raise ValueError(
            f"Desteklenmeyen dil: '{lang}'. "
            f"Gecerli secenekler: {SUPPORTED_LANGUAGES}"
        )
    return lang


def validate_stop_id(stop_id: str) -> str:
    """Durak ID'sini temel bicim kontrolunden gecirir."""
    if not stop_id or not isinstance(stop_id, str):
        raise ValueError("Durak ID'si bos olamaz.")
    return stop_id.strip()


def validate_coordinates(lat: float, lon: float) -> tuple[float, float]:
    """Enlem/boylam degerlerinin gecerli aralikta oldugunu kontrol eder."""
    if not (-90 <= lat <= 90):
        raise ValueError(f"Gecersiz enlem: {lat}. [-90, 90] araliginda olmali.")
    if not (-180 <= lon <= 180):
        raise ValueError(f"Gecersiz boylam: {lon}. [-180, 180] araliginda olmali.")
    return lat, lon
