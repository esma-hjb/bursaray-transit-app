"""Durak ve rota planlama ekranlari."""

from __future__ import annotations

from services.stop_service import StopService
from services.trip_planner import TripPlanner
from utils.exceptions import BursaTransitError
from utils.validators import validate_coordinates


class StopView:
    """Durak ve rota planlama ekranları."""

    def __init__(self):
        self._stop_svc = StopService()
        self._planner = TripPlanner()

    def show_nearby(self):
        """Kullanıcının giriş yaptığı koordinatlara yakın durakları gösterir."""
        print("\n  Yakındaki Duraklar")
        try:
            lat = float(input("  Enlem (orn. 40.1985): ").strip())
            lon = float(input("  Boylam (orn. 29.0610): ").strip())
            lat, lon = validate_coordinates(lat, lon)
        except ValueError as e:
            print(f"  [!]  {e}\n")
            return

        results = self._stop_svc.get_nearby_stops(lat, lon)
        if not results:
            results = self._stop_svc.get_nearby_stops(lat, lon, expanded=True)
            if results:
                print("  (Genisletilmis arama - 1500 m)")

        if not results:
            print("  Yakinda durak bulunamadi.\n")
            return

        print(f"\n  {'ID':<6} {'Durak Adi':<20} {'Mesafe':>8}")
        print("  " + "-" * 38)
        for stop, dist in results:
            print(f"  {stop.id:<6} {stop.name:<20} {dist:>6.0f} m")
        print()

    def show_trip_planner(self):
        """Başlangıç ve varış durakları arasında rota planlar ve gösterir."""
        print("\n   Rota Planlayici")
        origin = input("  Baslangic durak ID (orn. S001): ").strip().upper()
        dest = input("  Varis durak ID    (orn. S005): ").strip().upper()
        try:
            trip = self._planner.plan(origin, dest)
        except BursaTransitError as e:
            print(f"  [!]  {e}\n")
            return

        if not trip.steps:
            print("  [OK]  Zaten hedef duraktasiniz.\n")
            return

        print(f"\n  Toplam sure : {trip.total_duration_min} dk")
        print(f"  Toplam ucret: {trip.total_fare:.2f} TL\n")
        for i, step in enumerate(trip.steps, 1):
            print(
                f"  {i}. [{step.mode.upper()}] "
                f"{step.from_stop_id} -> {step.to_stop_id}"
            )
        print()
