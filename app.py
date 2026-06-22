"""Bursa Transit Web Arayüzü - Streamlit Uygulaması

Kullanıcı arayüzü bileşenleri:
- Durakları Listele
- Otobüsleri Listele
- Rota Planlama
- Canlı Otobüs Takibi
- Son Rotalar ve Favoriler
"""

import sys
from pathlib import Path

import requests
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from config import API_BASE_URL, API_TIMEOUT
from services.stop_service import StopService
from services.trip_planner import TripPlanner
from utils.exceptions import StopNotFoundError, NoRouteFoundError
from utils.trip_logger import save_trip, load_trips, save_all_trips
from utils.favorites import save_favorite, load_favorites

# ---------------- API ----------------
API_URL = f"{API_BASE_URL}/buses"
MOCK_BUSES = [
    {"route": "S001", "bus_id": "BUS101", "next_stop": "Görükle", "eta": 5},
    {"route": "S002", "bus_id": "BUS102", "next_stop": "Üniversite", "eta": 8},
]


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Bursa Transit App", page_icon="🚍", layout="wide")


# ---------------- HEADER ----------------
st.markdown(
    """
<h1 style='text-align:center; color:#4ade80;'>🚍 Bursa Transit App</h1>
<h4 style='text-align:center; color:gray;'>Akıllı Toplu Taşıma Sistemi</h4>
""",
    unsafe_allow_html=True,
)

st.markdown("---")


# ---------------- SIDEBAR ----------------
st.sidebar.title("🚍 Bursa Transit")

menu = st.sidebar.selectbox(
    "Menü", ["Durakları Listele", "Otobüsler", "Rota Planla", "Canlı Otobüs Takibi"]
)


stop_service = StopService()
trip_planner = TripPlanner()


# ---------------- STOPS ----------------
if menu == "Durakları Listele":

    st.header("📍 Tüm Duraklar")

    stops = stop_service.get_all_stops()

    for stop in stops:
        st.markdown(
            f"""
        <div style="
            padding:10px;
            margin:6px 0;
            border-radius:10px;
            background:#111827;
            color:white;
            border-left:4px solid #3b82f6;
        ">
            📍 <b>{stop.name}</b><br>
            🆔 {stop.id}
        </div>
        """,
            unsafe_allow_html=True,
        )


# ---------------- BUS LIST ----------------
elif menu == "Otobüsler":

    st.header("🚌 Otobüs Listesi")

    try:
        res = requests.get(API_URL, timeout=API_TIMEOUT)
        data = res.json()

        if not data:
            st.warning("Canlı veri alınamadı, mock veriler gösteriliyor.")
            data = MOCK_BUSES

    except requests.exceptions.RequestException:
        st.warning(
            "Canlı otobüs API'sine bağlanılamadı. Mock veriler gösteriliyor."
        )
        data = MOCK_BUSES

    if not data:
        st.warning("Veri yok")
    else:
        for bus in data:
            st.markdown(
                f"""
            <div style="
                padding:12px;
                margin:8px 0;
                border-radius:12px;
                background:linear-gradient(135deg,#1f2937,#111827);
                color:white;
                border-left:5px solid #3b82f6;
            ">
                🚌 <b>{bus['bus_id']}</b><br>
                🚏 {bus['route']}<br>
                📍 {bus['next_stop']}<br>
                ⏱ {bus['eta']} dk
            </div>
            """,
                unsafe_allow_html=True,
            )


# ---------------- ROUTE ----------------
elif menu == "Rota Planla":

    st.header("🗺️ Rota Planlama")

    stops = stop_service.get_all_stops()

    stop_names = {f"{s.name} ({s.id})": s.id for s in stops}

    origin = st.selectbox("Başlangıç", stop_names.keys())
    destination = st.selectbox("Varış", stop_names.keys())

    col1, col2 = st.columns(2)

    with col1:
        if st.button("⭐ Başlangıç"):
            save_favorite(stop_names[origin])

    with col2:
        if st.button("⭐ Varış"):
            save_favorite(stop_names[destination])

    if st.button("Rota Oluştur"):

        try:
            trip = trip_planner.plan(stop_names[origin], stop_names[destination])

            save_trip(trip)

            st.success("Rota bulundu!")

            col1, col2 = st.columns(2)
            col1.metric("⏱ Süre", f"{trip.total_duration_min} dk")
            col2.metric("💳 Ücret", f"{trip.total_fare} TL")

            st.markdown("### 🗺️ Adımlar")

            for i, step in enumerate(trip.steps, 1):
                st.markdown(
                    f"""
                <div style="
                    padding:10px;
                    margin:6px 0;
                    border-radius:10px;
                    background:#111827;
                    color:white;
                    border-left:4px solid #4ade80;
                ">
                    <b>{i}. Adım</b><br>
                    🚍 {step.mode}<br>
                    📍 {step.from_stop_id} ➜ {step.to_stop_id}
                </div>
                """,
                    unsafe_allow_html=True,
                )

        except StopNotFoundError:
            st.error("Durak bulunamadı")

        except NoRouteFoundError:
            st.error("Rota bulunamadı")


# ---------------- LIVE BUSES ----------------
elif menu == "Canlı Otobüs Takibi":

    st.header("🚍 Canlı Otobüs")

    try:
        res = requests.get(API_URL, timeout=API_TIMEOUT)
        data = res.json()

        if not data:
            st.warning("Canlı veri alınamadı, mock veriler gösteriliyor.")
            data = MOCK_BUSES

    except requests.exceptions.RequestException:
        st.warning(
            "Canlı otobüs API'sine bağlanılamadı. Mock veriler gösteriliyor."
        )
        data = MOCK_BUSES

    if not data:
        st.warning("Veri yok")
    else:
        for bus in data:
            st.markdown(
                f"""
            <div style="
                padding:12px;
                margin:8px 0;
                border-radius:12px;
                background:linear-gradient(135deg,#1f2937,#111827);
                color:white;
                border-left:5px solid #4ade80;
            ">
                🚍 {bus['route']}<br>
                🚌 {bus['bus_id']}<br>
                📍 {bus['next_stop']}<br>
                ⏱ {bus['eta']} dk
            </div>
            """,
                unsafe_allow_html=True,
            )


# ---------------- SIDEBAR HISTORY (FIXED DELETE) ----------------
st.sidebar.subheader("📜 Son Rotalar")

trips = load_trips()

if trips:

    history_start = max(0, len(trips) - 5)
    for i, t in enumerate(trips[-5:]):

        col1, col2 = st.sidebar.columns([5, 1])

        with col1:
            st.sidebar.caption(
                f"🚍 {t.get('from')} ➜ {t.get('to')} | ⏱ {t.get('duration')} dk"
            )

        with col2:
            if st.sidebar.button("🗑", key=f"del_{i}"):
                trips.pop(history_start + i)
                save_all_trips(trips)
                st.rerun()

else:
    st.sidebar.caption("Henüz rota yok")


# ---------------- FAVORITES ----------------
st.sidebar.subheader("⭐ Favoriler")

favs = load_favorites()

if favs:
    for f in favs:
        st.sidebar.caption(f"⭐ {f}")
else:
    st.sidebar.caption("Henüz favori yok")
