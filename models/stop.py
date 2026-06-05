"""Stop (Durak) veri modeli.

Bir toplu taşıma durağını temsil eder: kimlik, ad, konum (enlem/boylam)
ve o duraktan geçen hatların kimlikleri.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Stop:
    """Tek bir durağı temsil eder.

    Alanlar:
        id: Durağın benzersiz kimliği (örn. "S001").
        name: Durağın adı (örn. "Şehreküstü").
        lat: Enlem (latitude).
        lon: Boylam (longitude).
        line_ids: Bu duraktan geçen hatların kimlik listesi (örn. ["T1", "B12"]).
    """

    id: str
    name: str
    lat: float
    lon: float
    line_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Modeli JSON'a yazılabilir bir sözlüğe çevirir."""
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "line_ids": self.line_ids,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Stop":
        """JSON'dan okunan bir sözlükten Stop nesnesi oluşturur."""
        return cls(
            id=data["id"],
            name=data["name"],
            lat=float(data["lat"]),
            lon=float(data["lon"]),
            line_ids=list(data.get("line_ids", [])),
        )
