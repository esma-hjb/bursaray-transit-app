"""Stop (Durak) veri modeli.

Bir toplu tasima duragini temsil eder: kimlik, ad, konum (enlem/boylam)
ve o duraktan gecen hatlarin kimlikleri.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Stop:
    """Tek bir duragi temsil eder.

    Alanlar:
        id: Duragin benzersiz kimligi (orn. "S001").
        name: Duragin adi (orn. "Sehrekustu").
        lat: Enlem (latitude).
        lon: Boylam (longitude).
        line_ids: Bu duraktan gecen hatlarin kimlik listesi (orn. ["T1", "B12"]).
    """

    id: str
    name: str
    lat: float
    lon: float
    line_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Modeli JSON'a yazilabilir bir sozluge cevirir."""
        return {
            "id": self.id,
            "name": self.name,
            "lat": self.lat,
            "lon": self.lon,
            "line_ids": self.line_ids,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Stop":
        """JSON'dan okunan bir sozlukten Stop nesnesi olusturur."""
        return cls(
            id=data["id"],
            name=data["name"],
            lat=float(data["lat"]),
            lon=float(data["lon"]),
            line_ids=list(data.get("line_ids", [])),
        )
