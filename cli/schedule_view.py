"""Sefer tarifesi ekrani."""
from __future__ import annotations

from datetime import datetime

from services.schedule_service import ScheduleService
from utils.exceptions import BursaTransitError


class ScheduleView:
    def __init__(self):
        self._sched_svc = ScheduleService()

    def show(self):
        print("\n  Sefer Tarifesi")
        routes = self._sched_svc.all_routes()
        if not routes:
            print("  Tarife verisi bulunamadi.\n")
            return

        print("  Mevcut hatlar:", ", ".join(routes))
        route_id = input("  Hat ID girin (orn. T1): ").strip().upper()

        try:
            departures = self._sched_svc.get_departures(route_id)
        except BursaTransitError as e:
            print(f"  [!]  {e}\n")
            return

        now = datetime.now()
        nxt = self._sched_svc.next_departure(route_id, now)
        wait = self._sched_svc.wait_minutes(route_id, now)

        print(f"\n  {route_id} hatti kalkis saatleri:")
        for dep in departures:
            marker = " <-- SONRAKI" if dep == nxt else ""
            print(f"    {dep}{marker}")

        if nxt:
            print(f"\n  Sonraki sefer : {nxt}  (~{wait} dk sonra)")
        else:
            print("\n  Bugun baska sefer yok.")
        print()
