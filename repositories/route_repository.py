"""Hat (Route) verisine erisim katmani."""
from __future__ import annotations

from config import ROUTES_FILE
from models.route import Route
from repositories.base_repository import BaseRepository


class RouteRepository(BaseRepository):
    """Hatlari data/routes.json dosyasindan okuyup yazar."""

    file_path = ROUTES_FILE
    model_cls = Route

    def get_by_stop(self, stop_id):
        """Belirli bir duraktan gecen tum hatlari dondurur."""
        return [route for route in self.get_all() if stop_id in route.stop_ids]