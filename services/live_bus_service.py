"""Canlı Otobüs Takibi Servisi

Gerçek zamanlı otobüs konumu ve tahmini varış süresi bilgilerini sağlar.
API çalışmıyorsa otomatik olarak mock veriye geçer.
"""

import requests
from config import API_BASE_URL, API_TIMEOUT

# Mock veri — data/routes.json ile tutarlı gerçek hat ve durak ID'leri
MOCK_BUS_DATA = [
    {"route": "T1", "bus_id": "BUS101", "next_stop": "Şehreküstü",  "eta": 3},
    {"route": "M1", "bus_id": "BUS102", "next_stop": "Görükle",      "eta": 7},
    {"route": "B1", "bus_id": "BUS103", "next_stop": "Terminal",     "eta": 5},
    {"route": "B2", "bus_id": "BUS104", "next_stop": "Fethiye",      "eta": 9},
    {"route": "B3", "bus_id": "BUS105", "next_stop": "Nilüfer",      "eta": 4},
]


class LiveBusService:
    """Canlı otobüs verisi yönetimi."""

    def __init__(self):
        self.api_url = f"{API_BASE_URL}/buses"
        self.timeout = API_TIMEOUT

    def get_live_buses(self):
        """Aktif otobüslerin listesini döndürür.

        Önce gerçek API'yi dener. Bağlanamazsa (ya da hata alırsa)
        otomatik olarak mock veriye düşer — API başlatmaya gerek yoktur.
        """
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            if data:
                return data
        except Exception:
            pass  # API çalışmıyor, mock'a düş

        return MOCK_BUS_DATA
