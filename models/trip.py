"""Trip (Yolculuk/Rota plani) veri modeli.

Bir baslangic duragindan bir varis duragina planlanan yolculugu temsil eder.
Bir yolculuk bir veya birden cok adimdan (TripStep) olusur; her adim tek bir
hatla (veya yuruyerek) yapilan bir parcadir. Coklu-mod (otobus + metro + tramvay)
bu sayede gosterilebilir.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class TripStep:
    """Yolculugun tek bir adimi (orn. "T1 hattiyla S001'den S005'e").

    Alanlar:
        mode: Bu adimin modu (orn. "tram", "bus", "walk").
        from_stop_id: Adimin basladigi durak kimligi.
        to_stop_id: Adimin bittigi durak kimligi.
        route_id: Kullanilan hattin kimligi (yuruyus adiminda None olabilir).
        duration_min: Adimin tahmini suresi (dakika).
    """

    mode: str
    from_stop_id: str
    to_stop_id: str
    route_id: str | None = None
    duration_min: float = 0.0

    def to_dict(self) -> dict:
        return {
            "mode": self.mode,
            "from_stop_id": self.from_stop_id,
            "to_stop_id": self.to_stop_id,
            "route_id": self.route_id,
            "duration_min": self.duration_min,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TripStep":
        return cls(
            mode=data["mode"],
            from_stop_id=data["from_stop_id"],
            to_stop_id=data["to_stop_id"],
            route_id=data.get("route_id"),
            duration_min=float(data.get("duration_min", 0.0)),
        )


@dataclass
class Trip:
    """Planlanan bir yolculuk (adimlarin toplami).

    Alanlar:
        origin_stop_id: Baslangic duragi kimligi.
        destination_stop_id: Varis duragi kimligi.
        steps: Yolculugu olusturan adimlar (sirali).
        total_duration_min: Toplam tahmini sure (dakika).
        total_fare: Toplam tahmini ucret (TL).
    """

    origin_stop_id: str
    destination_stop_id: str
    steps: list[TripStep] = field(default_factory=list)
    total_duration_min: float = 0.0
    total_fare: float = 0.0

    def to_dict(self) -> dict:
        return {
            "origin_stop_id": self.origin_stop_id,
            "destination_stop_id": self.destination_stop_id,
            "steps": [step.to_dict() for step in self.steps],
            "total_duration_min": self.total_duration_min,
            "total_fare": self.total_fare,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Trip":
        return cls(
            origin_stop_id=data["origin_stop_id"],
            destination_stop_id=data["destination_stop_id"],
            steps=[TripStep.from_dict(s) for s in data.get("steps", [])],
            total_duration_min=float(data.get("total_duration_min", 0.0)),
            total_fare=float(data.get("total_fare", 0.0)),
        )
