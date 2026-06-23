"""Hat is mantigi servisi."""

from __future__ import annotations

from repositories.route_repository import RouteRepository
from repositories.stop_repository import StopRepository
from utils.exceptions import RouteNotFoundError


class RouteService:
    """Hat sorgulama islemlerini yonetir."""

    def __init__(self):
        self._route_repo = RouteRepository()
        self._stop_repo = StopRepository()

    def get_all_routes(self):
        """Tum hatlari dondurur."""
        return self._route_repo.get_all()

    def get_route_by_id(self, route_id: str):
        """ID'ye gore hat dondurur; bulunamazsa RouteNotFoundError firlatir."""
        route = self._route_repo.get_by_id(route_id)
        if route is None:
            raise RouteNotFoundError(route_id)
        return route

    def get_stops_for_route(self, route_id: str):
        """Belirli bir hattin sirali durak listesini dondurur."""
        route = self.get_route_by_id(route_id)
        stops = []
        for sid in route.stop_ids:
            stop = self._stop_repo.get_by_id(sid)
            if stop:
                stops.append(stop)
        return stops
