"""Sefer tarifesi servisi.

data/schedule.json dosyasindaki hat kalki saatlerini okur ve
verilen saate gore "sonraki sefer" hesaplar.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from config import SCHEDULE_FILE
from storage.json_storage import read_json
from utils.exceptions import RouteNotFoundError


class ScheduleService:
    """Hat sefer saatlerini sorgular."""

    def __init__(self):
        self._data: dict[str, list[str]] = read_json(SCHEDULE_FILE, default={})

    def get_departures(self, route_id: str) -> list[str]:
        """Bir hattin tum kalkis saatlerini dondurur (HH:MM listesi).

        Raises:
            RouteNotFoundError: Hat tarifede yoksa.
        """
        if route_id not in self._data:
            raise RouteNotFoundError(route_id)
        return list(self._data[route_id])

    def next_departure(self, route_id: str, now: datetime | None = None) -> str | None:
        """Verilen andan sonraki ilk kalkis saatini dondurur.

        Args:
            route_id: Sorgulanacak hat ID'si.
            now: Referans zaman; None ise datetime.now() kullanilir.

        Returns:
            'HH:MM' formatinda sonraki sefer, yoksa None.
        """
        if route_id not in self._data:
            return None

        if now is None:
            now = datetime.now()

        current_minutes = now.hour * 60 + now.minute

        for dep in sorted(self._data[route_id]):
            h, m = map(int, dep.split(":"))
            dep_minutes = h * 60 + m
            if dep_minutes >= current_minutes:
                return dep

        return None  # Bugunkü son sefer gecti

    def wait_minutes(self, route_id: str, now: datetime | None = None) -> int | None:
        """Sonraki sefere kac dakika kaldigini dondurur.

        Returns:
            Dakika cinsinden bekleme suresi, ya da None (sefer yok).
        """
        nxt = self.next_departure(route_id, now)
        if nxt is None:
            return None
        if now is None:
            now = datetime.now()
        h, m = map(int, nxt.split(":"))
        dep_minutes = h * 60 + m
        current_minutes = now.hour * 60 + now.minute
        return dep_minutes - current_minutes

    def all_routes(self) -> list[str]:
        """Tarifede kayitli tum hat ID'lerini dondurur."""
        return list(self._data.keys())
