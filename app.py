import streamlit as st

from services.stop_service import StopService
from services.trip_planner import TripPlanner
from utils.exceptions import StopNotFoundError, NoRouteFoundError

from utils.trip_logger import save_trip, load_trips
from utils.favorites import save_favorite, load_favorites


st.set_page_config(
    page_title="Bursa Transit App",
    page_icon="🚍",
    layout="wide"
)

st.title("🚍 Bursa Transit App")
st.subheader("Bursa Toplu Taşıma Rota Planlama Sistemi")


# ---------------- SERVICES ----------------
stop_service = StopService()
trip_planner = TripPlanner()


# ---------------- MENU ----------------
menu = st.sidebar.selectbox(
    "Menü",
    ["Durakları Listele", "Rota Planla"]
)


# ---------------- STOPS ----------------
if menu == "Durakları Listele":

    st.header("📍 Tüm Duraklar")

    stops = stop_service.get_all_stops()

    for stop in stops:
        st.write(f"**{stop.name}** ({stop.id})")


# ---------------- ROUTE ----------------
elif menu == "Rota Planla":

    st.header("🗺️ Rota Planlama")

    stops = stop_service.get_all_stops()

    stop_names = {
        f"{stop.name} ({stop.id})": stop.id
        for stop in stops
    }

    origin = st.selectbox("Başlangıç Durağı", stop_names.keys())
    destination = st.selectbox("Varış Durağı", stop_names.keys())

    # ⭐ FAVORİ (DÜZELTİLMİŞ)
    col1, col2 = st.columns(2)

    with col1:
        if st.button("⭐ Başlangıcı Favorile"):
            save_favorite(stop_names[origin])
            st.success("Başlangıç favorilere eklendi")

    with col2:
        if st.button("⭐ Varışını Favorile"):
            save_favorite(stop_names[destination])
            st.success("Varış favorilere eklendi")


    # ---------------- ROUTE ----------------
    if st.button("Rota Oluştur"):

        try:
            trip = trip_planner.plan(
                stop_names[origin],
                stop_names[destination]
            )

            save_trip(trip)

            st.success("Rota bulundu!")

            st.metric("⏱ Süre", f"{trip.total_duration_min} dk")
            st.metric("💳 Ücret", f"{trip.total_fare} TL")

            st.subheader("🗺️ Rota Adımları")

            for i, step in enumerate(trip.steps, 1):
                st.markdown(f"""
                <div style="
                    padding:10px;
                    margin:8px 0;
                    border-radius:10px;
                    background:#1f2937;
                    color:white;
                    border-left:4px solid #4ade80;
                ">
                    <b>Step {i}</b><br>
                    🚍 {step.mode.upper()}<br>
                    📍 {step.from_stop_id} ➜ {step.to_stop_id}
                </div>
                """, unsafe_allow_html=True)

        except StopNotFoundError:
            st.error("Durak bulunamadı.")

        except NoRouteFoundError:
            st.error("Rota bulunamadı.")

        except Exception as e:
            st.error(f"Hata: {e}")


# ---------------- SIDEBAR HISTORY ----------------
st.sidebar.subheader("📜 Son Rotalar")

trips = load_trips()

if trips:
    for t in trips[-5:]:
        st.sidebar.write(f"🚍 {t.get('from')} ➜ {t.get('to')} | ⏱ {t.get('duration')} dk")
else:
    st.sidebar.write("Henüz rota yok.")


# ---------------- SIDEBAR FAVORITES ----------------
st.sidebar.subheader("⭐ Favoriler")

favs = load_favorites()

if favs:
    for f in favs:
        st.sidebar.write(f"⭐ {f}")
else:
    st.sidebar.write("Henüz favori yok.")