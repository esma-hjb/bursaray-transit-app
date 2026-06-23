"""Rota Planlama Servisi

Başlangıç ve varış durakları arasında BFS algoritmasıyla optimal rota hesaplar.
"""

from collections import deque

from models.trip import Trip, TripStep
from repositories.route_repository import RouteRepository
from repositories.stop_repository import StopRepository
from utils.exceptions import StopNotFoundError, NoRouteFoundError


class TripPlanner:
    """BFS tabanlı rota planlayıcı."""

    def __init__(self):
        self._stop_repo = StopRepository()
        self._route_repo = RouteRepository()

    def plan(self, origin_id: str, destination_id: str) -> Trip:
        origin = self._stop_repo.get_by_id(origin_id)
        if origin is None:
            raise StopNotFoundError(origin_id)
        dest = self._stop_repo.get_by_id(destination_id)
        if dest is None:
            raise StopNotFoundError(destination_id)

        if origin_id == destination_id:
            return Trip(
                origin_stop_id=origin_id,
                destination_stop_id=destination_id,
                steps=[],
                total_duration_min=0.0,
                total_fare=0.0,
            )

        routes = self._route_repo.get_all()

        # Hat grafiği: durak -> [(komşu_durak, route_id, mod)]
        graph: dict[str, list[tuple[str, str, str]]] = {}
        for route in routes:
            stops = route.stop_ids
            for i in range(len(stops) - 1):
                a, b = stops[i], stops[i + 1]
                graph.setdefault(a, []).append((b, route.id, route.mode.value))
                graph.setdefault(b, []).append((a, route.id, route.mode.value))

        # BFS
        queue = deque()
        queue.append((origin_id, []))
        visited = {origin_id}

        while queue:
            current, path = queue.popleft()
            for neighbor, route_id, mode in graph.get(current, []):
                if neighbor in visited:
                    continue
                new_path = path + [TripStep(
                    mode=mode,
                    from_stop_id=current,
                    to_stop_id=neighbor,
                    route_id=route_id,
                    duration_min=5.0,
                )]
                if neighbor == destination_id:
                    total_dur = len(new_path) * 5.0
                    total_fare = 15.0 if len(new_path) <= 2 else 15.0 + (len(new_path) - 2) * 5.0
                    return Trip(
                        origin_stop_id=origin_id,
                        destination_stop_id=destination_id,
                        steps=new_path,
                        total_duration_min=total_dur,
                        total_fare=total_fare,
                    )
                visited.add(neighbor)
                queue.append((neighbor, new_path))

        raise NoRouteFoundError(origin_id, destination_id)
