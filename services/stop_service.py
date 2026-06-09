"""Durak is mantigi servisi."""
from __future__ import annotations

from config import NEARBY_RADIUS_M, NEARBY_RADIUS_EXPANDED_M
from repositories.stop_repository import StopRepository
from repositories.route_repository import RouteRepository
from utils.exceptions import StopNotFoundError
from utils.geo_utils import stops_within_radius


class StopService:
    """Durak sorgulama ve yakin durak bulma islemlerini yonetir."""

    def __init__(self):
        self._stop_repo = StopRepository()
        self._route_repo = RouteRepository()

    def get_all_stops(self):
        """Tum duraklari dondurur."""
        return self._stop_repo.get_all()

    def get_stop_by_id(self, stop_id: str):
        """ID'ye gore durak dondurur; bulunamazsa StopNotFoundError firlatir."""
        stop = self._stop_repo.get_by_id(stop_id)
        if stop is None:
            raise StopNotFoundError(stop_id)
        return stop

    def get_nearby_stops(self, lat: float, lon: float, expanded: bool = False):
        """Verilen konuma yakin duraklari dondurur.

        Args:
            lat, lon: Kullanici konumu.
            expanded: True ise genisletilmis yaricap kullanilir.

        Returns:
            (Stop, mesafe_metre) ciftlerinin listesi, yakindan uzaga sirali.
        """
        radius = NEARBY_RADIUS_EXPANDED_M if expanded else NEARBY_RADIUS_M
        all_stops = self._stop_repo.get_all()
        return stops_within_radius(all_stops, lat, lon, radius)

    def get_routes_for_stop(self, stop_id: str):
        """Belirli bir duraktan gecen hatlari dondurur."""
        self.get_stop_by_id(stop_id)  # var mi kontrol et
        return self._route_repo.get_by_stop(stop_id)
