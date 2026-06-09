"""Rota planlama servisi.

Baslangic duragindan varis duragina en basit (en az aktarmali) rotayi
BFS (Breadth-First Search) algoritmasiyla bulur.

Cift-yon destegi: Her hat hem ileri hem geri yonde aranir.
Schedule entegrasyonu: plan_with_schedule() bir zaman girer, sonraki
seferi hesaplar.
"""
from __future__ import annotations

from collections import deque
from datetime import datetime, timedelta

from models.trip import Trip, TripStep
from repositories.route_repository import RouteRepository
from repositories.stop_repository import StopRepository
from utils.exceptions import StopNotFoundError, NoRouteFoundError


# Hat modu basina tahmini dakika/durak katsayisi (gercek API'ye kadar)
_DURATION_PER_STOP: dict[str, float] = {
    "tram": 2.0,
    "metro": 2.5,
    "bus": 3.5,
    "walk": 5.0,
}

# Hat modu basina tahmini ucret (TL)
_FARE_PER_RIDE: dict[str, float] = {
    "tram": 15.0,
    "metro": 15.0,
    "bus": 15.0,
    "walk": 0.0,
}


class TripPlanner:
    """Duraklar arasi rota planlama islemlerini yurutur."""

    def __init__(self):
        self._stop_repo = StopRepository()
        self._route_repo = RouteRepository()

    def plan(self, origin_id: str, destination_id: str) -> Trip:
        """Baslangic -> varis icin en kisa (aktarma bazli) rotayi dondurur.

        BFS cift yonlu: her hat hem ileri (idx+1) hem geri (idx-1) taranir.

        Args:
            origin_id: Baslangic duragi ID'si.
            destination_id: Varis duragi ID'si.

        Returns:
            Adimlarla dolu bir Trip nesnesi.

        Raises:
            StopNotFoundError: Baslangic veya varis duragi bulunamazsa.
            NoRouteFoundError: Iki durak arasinda baglanti yoksa.
        """
        # Duraklarin varligini dogrula
        origin = self._stop_repo.get_by_id(origin_id)
        if origin is None:
            raise StopNotFoundError(origin_id)
        dest = self._stop_repo.get_by_id(destination_id)
        if dest is None:
            raise StopNotFoundError(destination_id)

        if origin_id == destination_id:
            return Trip(origin_stop_id=origin_id, destination_stop_id=destination_id)

        # Durak -> hat haritasi (hizli erisim icin)
        routes = self._route_repo.get_all()
        stop_to_routes: dict[str, list] = {}
        for route in routes:
            for sid in route.stop_ids:
                stop_to_routes.setdefault(sid, []).append(route)

        # BFS: her dugum (durak_id, rota_adimlari_listesi)
        queue: deque[tuple[str, list[TripStep]]] = deque()
        queue.append((origin_id, []))
        visited: set[str] = {origin_id}

        while queue:
            current_id, steps = queue.popleft()

            for route in stop_to_routes.get(current_id, []):
                idx = route.stop_ids.index(current_id)
                mode = route.mode.value

                # Hem ileri (+1) hem geri (-1) yonde komsu duraklari dene
                directions = []
                if idx + 1 < len(route.stop_ids):
                    directions.append(("forward", range(idx + 1, len(route.stop_ids))))
                if idx - 1 >= 0:
                    directions.append(("backward", range(idx - 1, -1, -1)))

                for _dir, indices in directions:
                    for next_idx in indices:
                        next_id = route.stop_ids[next_idx]
                        stops_traveled = abs(next_idx - idx)
                        step = TripStep(
                            mode=mode,
                            from_stop_id=current_id,
                            to_stop_id=next_id,
                            route_id=route.id,
                            duration_min=stops_traveled * _DURATION_PER_STOP.get(mode, 3.0),
                        )
                        new_steps = steps + [step]

                        if next_id == destination_id:
                            return self._build_trip(origin_id, destination_id, new_steps)

                        if next_id not in visited:
                            visited.add(next_id)
                            queue.append((next_id, new_steps))

        raise NoRouteFoundError(origin_id, destination_id)

    # ------------------------------------------------------------------
    # Yardimci
    # ------------------------------------------------------------------

    @staticmethod
    def _build_trip(origin_id: str, dest_id: str, steps: list[TripStep]) -> Trip:
        total_dur = sum(s.duration_min for s in steps)
        # Her benzersiz hat icin bir ucret
        seen_routes: set[str] = set()
        total_fare = 0.0
        for s in steps:
            if s.route_id and s.route_id not in seen_routes:
                seen_routes.add(s.route_id)
                total_fare += _FARE_PER_RIDE.get(s.mode, 15.0)
        return Trip(
            origin_stop_id=origin_id,
            destination_stop_id=dest_id,
            steps=steps,
            total_duration_min=round(total_dur, 1),
            total_fare=round(total_fare, 2),
        )
