"""Durak (Stop) verisine erisim katmani."""

from __future__ import annotations

from config import STOPS_FILE
from models.stop import Stop
from repositories.base_repository import BaseRepository


class StopRepository(BaseRepository):
    """Duraklari data/stops.json dosyasindan okuyup yazar."""

    file_path = STOPS_FILE
    model_cls = Stop

    def get_by_line(self, line_id):
        """Belirli bir hattin gectigi tum duraklari dondurur."""
        return [stop for stop in self.get_all() if line_id in stop.line_ids]
