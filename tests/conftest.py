"""Pytest fixture'lari - test izolasyonu icin gecici JSON dosyalari."""
from __future__ import annotations

import json
import pytest
from pathlib import Path


@pytest.fixture
def tmp_stops(tmp_path):
    """Gecici stops.json dondurur."""
    data = [
        {"id": "S001", "name": "Sehrekustu", "lat": 40.1985, "lon": 29.0610, "line_ids": ["T1", "B1"]},
        {"id": "S002", "name": "Heykel", "lat": 40.1828, "lon": 29.0617, "line_ids": ["T1"]},
        {"id": "S003", "name": "Kulturpark", "lat": 40.1955, "lon": 29.0480, "line_ids": ["T1", "B1"]},
        {"id": "S005", "name": "Acemler", "lat": 40.2050, "lon": 28.9900, "line_ids": ["M1", "B1"]},
    ]
    f = tmp_path / "stops.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    return f


@pytest.fixture
def tmp_routes(tmp_path):
    """Gecici routes.json dondurur."""
    data = [
        {"id": "T1", "name": "Sehrekustu - Heykel", "mode": "tram", "stop_ids": ["S001", "S003", "S002"]},
        {"id": "B1", "name": "Kulturpark - Acemler", "mode": "bus", "stop_ids": ["S003", "S001", "S005"]},
    ]
    f = tmp_path / "routes.json"
    f.write_text(json.dumps(data), encoding="utf-8")
    return f
