"""Bursa Transit Ana Menü

CLI arayüzünün ana menü sistemi. Kullanıcı seçimlerine göre ilgili
fonksiyonları çağırır.
"""

from cli.stop_view import StopView
from cli.route_view import RouteView
from cli.settings_view import SettingsView
from cli.schedule_view import ScheduleView
from services.live_bus_service import LiveBusService


class MainMenu:
    """Ana menü yönetimi.

    Kullanıcı seçimlerine göre ilgili CLI görünümlerini yönetir.
    """

    MENU = {
        "1": ("Yakindaki Duraklar", "_nearby"),
        "2": ("Hat Detayi", "_route_detail"),
        "3": ("Rota Planla", "_plan_trip"),
        "4": ("Sefer Tarifesi", "_schedule"),
        "5": ("Ayarlar", "_settings"),
        "6": ("Canli Otobus Takibi", "_live_buses"),
        "0": ("Cikis", "_exit"),
    }

    def __init__(self):
        self._stop_view = StopView()
        self._route_view = RouteView()
        self._settings_view = SettingsView()
        self._schedule_view = ScheduleView()
        self._live_bus_service = LiveBusService()
        self._running = True

    def run(self):
        print("\n=== BURSA TRANSIT UYGULAMASI ===\n")

        while self._running:
            self._print_menu()
            choice = input("Seciminiz: ").strip()

            entry = self.MENU.get(choice)

            if entry is None:
                print("\n[!] Gecersiz secim. Lutfen yeniden deneyin.\n")
                continue

            getattr(self, entry[1])()

    def _print_menu(self):
        print("-" * 35)
        for key, (label, _) in self.MENU.items():
            print(f"[{key}] {label}")
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
        print("Gorusuruz!")
        self._running = False

    def _live_buses(self):
        try:
            buses = self._live_bus_service.get_live_buses()

            if not buses:
                print("\n[!] Canli otobus verisi bulunamadi.\n")
                return

            print("\n=== Canli Otobus Bilgileri ===\n")

            for bus in buses:
                print(
                    f"Hat: {bus['route']} | "
                    f"Otobus: {bus['bus_id']} | "
                    f"Durak: {bus['next_stop']} | "
                    f"Varis: {bus['eta']} dk"
                )

        except Exception as e:
            print("[HATA]:", e)
