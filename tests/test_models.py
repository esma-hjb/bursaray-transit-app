"""Model sinifi testleri."""

from models.route import Route, TransportMode
from models.stop import Stop
from models.trip import Trip, TripStep
from models.user_prefs import UserPrefs


def test_stop_roundtrip():
    s = Stop(id="S001", name="Test", lat=40.0, lon=29.0, line_ids=["T1"])
    assert Stop.from_dict(s.to_dict()) == s


def test_route_roundtrip():
    r = Route(id="T1", name="Hat", mode=TransportMode.TRAM, stop_ids=["S001", "S002"])
    assert Route.from_dict(r.to_dict()) == r


def test_trip_step_roundtrip():
    step = TripStep(
        mode="tram",
        from_stop_id="S001",
        to_stop_id="S002",
        route_id="T1",
        duration_min=4.0,
    )
    assert TripStep.from_dict(step.to_dict()) == step


def test_trip_total():
    steps = [
        TripStep("tram", "S001", "S002", "T1", 4.0),
        TripStep("bus", "S002", "S003", "B1", 7.0),
    ]
    trip = Trip("S001", "S003", steps=steps, total_duration_min=11.0, total_fare=30.0)
    assert trip.total_duration_min == 11.0
    assert trip.total_fare == 30.0


def test_user_prefs_defaults():
    p = UserPrefs()
    assert p.is_premium is False
    assert p.favorite_stop_ids == []
