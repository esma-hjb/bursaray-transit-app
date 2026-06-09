"""Uygulama genelinde kullanilan ozel istisna siniflari."""


class BursaTransitError(Exception):
    """Tum uygulama hatalarinin taban sinifi."""


class StopNotFoundError(BursaTransitError):
    """Verilen ID'ye sahip durak bulunamadiginda firlatilir."""

    def __init__(self, stop_id: str):
        super().__init__(f"Durak bulunamadi: '{stop_id}'")
        self.stop_id = stop_id


class RouteNotFoundError(BursaTransitError):
    """Verilen ID'ye sahip hat bulunamadiginda firlatilir."""

    def __init__(self, route_id: str):
        super().__init__(f"Hat bulunamadi: '{route_id}'")
        self.route_id = route_id


class NoRouteFoundError(BursaTransitError):
    """Baslangic -> varis arasinda rota bulunamadiginda firlatilir."""

    def __init__(self, origin_id: str, dest_id: str):
        super().__init__(
            f"Rota bulunamadi: '{origin_id}' -> '{dest_id}'"
        )
        self.origin_id = origin_id
        self.dest_id = dest_id


class StorageError(BursaTransitError):
    """JSON okuma/yazma hatalarinda firlatilir."""
