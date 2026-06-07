"""Route (Hat) veri modeli.

Bir toplu tasima hattini temsil eder: kimlik, ad, ulasim modu
(otobus / metro / tramvay) ve hattin ugradigi duraklarin sirasi.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TransportMode(str, Enum):
    """Ulasim modu. (str'den turedigi icin JSON'a dogrudan yazilabilir.)"""

    BUS = "bus"        # otobus
    METRO = "metro"    # metro
    TRAM = "tram"      # tramvay


@dataclass
class Route:
    """Tek bir hatti temsil eder.

    Alanlar:
        id: Hattin benzersiz kimligi (orn. "T1").
        name: Hattin adi (orn. "Emek - Sehrekustu").
        mode: Ulasim modu (TransportMode.BUS/METRO/TRAM).
        stop_ids: Hattin ugradigi duraklarin kimlikleri (sirali liste).
    """

    id: str
    name: str
    mode: TransportMode = TransportMode.BUS
    stop_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Modeli JSON'a yazilabilir bir sozluge cevirir."""
        return {
            "id": self.id,
            "name": self.name,
            "mode": self.mode.value,
            "stop_ids": self.stop_ids,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Route":
        """JSON'dan okunan bir sozlukten Route nesnesi olusturur."""
        return cls(
            id=data["id"],
            name=data["name"],
            mode=TransportMode(data.get("mode", "bus")),
            stop_ids=list(data.get("stop_ids", [])),
        )
