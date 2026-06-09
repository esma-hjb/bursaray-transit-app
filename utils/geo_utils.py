"""Cografi hesaplama yardimcilari.

Dis kutuphane gerektirmeden Haversine formuluyle iki koordinat arasindaki
mesafeyi metre cinsinden hesaplar. Faz 5'teki "yakin durak" ozelliginde
ve rota planlamada kullanilir.
"""
from __future__ import annotations

import math


# Dunya yaricapi (metre)
_EARTH_RADIUS_M = 6_371_000


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Iki koordinat arasindaki mesafeyi Haversine formuluyle hesaplar.

    Args:
        lat1, lon1: Birinci noktanin enlemi ve boylami (derece).
        lat2, lon2: Ikinci noktanin enlemi ve boylami (derece).

    Returns:
        Metre cinsinden duzlem yuzeyi mesafesi.
    """
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    d_phi = math.radians(lat2 - lat1)
    d_lambda = math.radians(lon2 - lon1)

    a = (
        math.sin(d_phi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(d_lambda / 2) ** 2
    )
    return _EARTH_RADIUS_M * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def stops_within_radius(stops, lat: float, lon: float, radius_m: float) -> list:
    """Verilen koordinata belirli bir yaricap icindeki duraklari dondurur.

    Args:
        stops: Stop nesnelerinin listesi (lat/lon alani olan).
        lat, lon: Merkez koordinat.
        radius_m: Arama yaricapi (metre).

    Returns:
        (stop, distance_m) ciftlerinin listesi, mesafeye gore sirali.
    """
    results = []
    for stop in stops:
        dist = haversine_distance(lat, lon, stop.lat, stop.lon)
        if dist <= radius_m:
            results.append((stop, dist))
    results.sort(key=lambda x: x[1])
    return results
