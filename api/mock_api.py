"""Mock API Sunucusu - Otobüs Canlı Takibi

Gerçek bir transit API gibi davranır:
- Her istekte ETA değerleri rastgele değişir (gerçek zamanlı his)
- /buses        → tüm aktif otobüsler
- /buses/<id>   → tek otobüs detayı
- /routes       → hat listesi
- /health       → sunucu sağlık kontrolü
"""

import random
from flask import Flask, jsonify

app = Flask(__name__)

# --- Sabit otobüs filosu ---
BUS_FLEET = [
    {"bus_id": "BUS101", "route": "T1", "next_stop": "Görükle",    "status": "active"},
    {"bus_id": "BUS102", "route": "M1", "next_stop": "Üniversite", "status": "active"},
    {"bus_id": "BUS103", "route": "B1", "next_stop": "Kültürpark", "status": "active"},
    {"bus_id": "BUS104", "route": "T2", "next_stop": "Osmangazi",  "status": "active"},
    {"bus_id": "BUS105", "route": "M2", "next_stop": "Nilüfer",    "status": "active"},
]

ROUTES = [
    {"route_id": "T1", "name": "Tramvay 1", "start": "Görükle",    "end": "Şehir Merkezi"},
    {"route_id": "M1", "name": "Metro 1",   "start": "Üniversite", "end": "Emek"},
    {"route_id": "B1", "name": "Otobüs 1",  "start": "Kültürpark", "end": "Kestel"},
    {"route_id": "T2", "name": "Tramvay 2", "start": "Osmangazi",  "end": "Mudanya"},
    {"route_id": "M2", "name": "Metro 2",   "start": "Nilüfer",    "end": "Bursa"},
]


def _with_random_eta(bus: dict) -> dict:
    """Her istekte ETA'yı 1-15 dk arasında rastgele değiştirir."""
    return {**bus, "eta": random.randint(1, 15)}


@app.route("/buses")
def get_buses():
    return jsonify([_with_random_eta(b) for b in BUS_FLEET])


@app.route("/buses/<bus_id>")
def get_bus(bus_id: str):
    bus = next((b for b in BUS_FLEET if b["bus_id"] == bus_id), None)
    if bus is None:
        return jsonify({"error": f"{bus_id} bulunamadı"}), 404
    return jsonify(_with_random_eta(bus))


@app.route("/routes")
def get_routes():
    return jsonify(ROUTES)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "bursa-transit-mock-api"})


if __name__ == "__main__":
    print("🚍 Mock API başlatılıyor → http://127.0.0.1:5000")
    app.run(debug=False, port=5000)
