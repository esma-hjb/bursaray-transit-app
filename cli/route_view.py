"""Hat detay ekrani."""

from __future__ import annotations

from services.route_service import RouteService
from utils.exceptions import BursaTransitError


class RouteView:
    def __init__(self):
        self._route_svc = RouteService()

    def show_route_detail(self):
        print("\n  Hat Detayi")
        routes = self._route_svc.get_all_routes()
        print("  Mevcut hatlar:")
        for r in routes:
            print(f"    {r.id}  -  {r.name}  [{r.mode.value}]")

        route_id = input("\n  Hat ID girin: ").strip().upper()
        try:
            stops = self._route_svc.get_stops_for_route(route_id)
        except BursaTransitError as e:
            print(f"  [!]  {e}\n")
            return

        print(f"\n  {'Sira':<5} {'ID':<6} {'Durak Adi'}")
        print("  " + "-" * 30)
        for i, stop in enumerate(stops, 1):
            print(f"  {i:<5} {stop.id:<6} {stop.name}")
        print()
