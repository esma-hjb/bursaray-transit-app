"""Route (Hat) veri modeli.

Bir toplu taşıma hattını temsil eder: kimlik, ad, ulaşım modu
(otobüs / metro / tramvay) ve hattın uğradığı durakların sırası.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TransportMode(str, Enum):
    """Ulaşım modu. (str'den türediği için JSON'a doğrudan yazılabilir.)"""

    BUS = "bus"        # otobüs
    METRO = "metro"    # metro
    TRAM = "tram"      # tramvay


@dataclass
class Route:
    """Tek bir hattı temsil eder.

    Alanlar:
        id: Hattın benzersiz kimliği (örn. "T1").
        name: Hattın adı (örn. "Emek - Şehreküstü").
        mode: Ulaşım modu (TransportMode.BUS/METRO/TRAM).
        stop_ids: Hattın uğradığı durakların kimlikleri (sıralı liste).
    """

    id: str
    name: str
    mode: TransportMode = TransportMode.BUS
    stop_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Modeli JSON'a yazılabilir bir sözlüğe çevirir."""
        return {
            "id": self.id,
            "name": self.name,
            "mode": self.mode.value,
            "stop_ids": self.stop_ids,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Route":
        """JSON'dan okunan bir sözlükten Route nesnesi oluşturur."""
        return cls(
            id=data["id"],
            name=data["name"],
            mode=TransportMode(data.get("mode", "bus")),
            stop_ids=list(data.get("stop_ids", [])),
        )
