"""Canlı Otobüs Takibi Servisi

Gerçek zamanlı otobüs konumu ve tahmini varış süresi bilgilerini sağlar.
"""

import requests
from config import API_BASE_URL, API_TIMEOUT


class LiveBusService:
    """Canlı otobüs verisi yönetimi."""

    def __init__(self):
        self.api_url = f"{API_BASE_URL}/buses"
        self.timeout = API_TIMEOUT

    def get_live_buses(self):
        """Aktif otobüslerin listesini API'den döndürür.

        Returns:
            Otobüs bilgilerini içeren sözlüklerin listesi.
        """
        try:
            response = requests.get(self.api_url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # API erişilemezse fallback mock data döndür
            print(f"[UYARI] API'ye ulaşılamadı: {e}")
            return [
                {"route": "T1", "bus_id": "BUS101", "next_stop": "Görükle", "eta": 5},
                {"route": "M1", "bus_id": "BUS102", "next_stop": "Üniversite", "eta": 8},
            ]
