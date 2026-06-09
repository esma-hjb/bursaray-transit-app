"""Ana menu - uygulamanin giris ekrani."""
from __future__ import annotations

from cli.stop_view import StopView
from cli.route_view import RouteView
from cli.settings_view import SettingsView
from cli.schedule_view import ScheduleView


class MainMenu:
    """Kullaniciya ana secenekleri sunan dongu."""

    MENU = {
        "1": ("Yakindaki Duraklar", "_nearby"),
        "2": ("Hat Detayi", "_route_detail"),
        "3": ("Rota Planla", "_plan_trip"),
        "4": ("Sefer Tarifesi", "_schedule"),
        "5": ("Ayarlar", "_settings"),
        "0": ("Cikis", "_exit"),
    }

    def __init__(self):
        self._stop_view = StopView()
        self._route_view = RouteView()
        self._settings_view = SettingsView()
        self._schedule_view = ScheduleView()
        self._running = True

    def run(self):
        print("\n  Bursaray Transit App'e Hos Geldiniz!\n")
        while self._running:
            self._print_menu()
            choice = input("Seciminiz: ").strip()
            entry = self.MENU.get(choice)
            if entry is None:
                print("  [!]  Gecersiz secim.\n")
                continue
            getattr(self, entry[1])()

    def _print_menu(self):
        print("-" * 35)
        for key, (label, _) in self.MENU.items():
            print(f"  [{key}] {label}")
        print("-" * 35)

    def _nearby(self):
        self._stop_view.show_nearby()

    def _route_detail(self):
        self._route_view.show_route_detail()

    def _plan_trip(self):
        self._stop_view.show_trip_planner()

    def _schedule(self):
        self._schedule_view.show()

    def _settings(self):
        self._settings_view.show()

    def _exit(self):
        print("\nGorusuruz! \n")
        self._running = False
