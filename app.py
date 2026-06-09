import streamlit as st

from services.stop_service import StopService
from services.trip_planner import TripPlanner
from utils.exceptions import StopNotFoundError, NoRouteFoundError


st.set_page_config(
    page_title="Bursa Transit App",
    page_icon="🚍",
    layout="wide"
)

st.title("🚍 Bursa Transit App")
st.subheader("Bursa Toplu Taşıma Rota Planlama Sistemi")


stop_service = StopService()
trip_planner = TripPlanner()

menu = st.sidebar.selectbox(
    "Menü",
    [
        "Durakları Listele",
        "Rota Planla"
    ]
)


if menu == "Durakları Listele":

    st.header("📍 Tüm Duraklar")

    stops = stop_service.get_all_stops()

    for stop in stops:
        st.write(f"**{stop.name}** ({stop.id})")


elif menu == "Rota Planla":

    st.header("🗺️ Rota Planlama")

    stops = stop_service.get_all_stops()

    stop_names = {
        f"{stop.name} ({stop.id})": stop.id
        for stop in stops
    }

    origin = st.selectbox(
        "Başlangıç Durağı",
        stop_names.keys()
    )

    destination = st.selectbox(
        "Varış Durağı",
        stop_names.keys()
    )

    if st.button("Rota Oluştur"):

        try:

            trip = trip_planner.plan(
                stop_names[origin],
                stop_names[destination]
            )

            st.success("Rota bulundu!")

            st.write(
                f"⏱️ Toplam Süre: {trip.total_duration_min} dk"
            )

            st.write(
                f"💳 Toplam Ücret: {trip.total_fare} TL"
            )

            st.subheader("Rota Detayları")

            for i, step in enumerate(trip.steps, 1):

                st.write(
                    f"{i}. {step.mode.upper()} | "
                    f"{step.from_stop_id} ➜ {step.to_stop_id}"
                )

        except StopNotFoundError:
            st.error("Durak bulunamadı.")

        except NoRouteFoundError:
            st.error("Bu iki durak arasında rota bulunamadı.")

        except Exception as e:
            st.error(f"Hata oluştu: {e}")