"""Servis katmani testleri."""

import pytest
from unittest.mock import MagicMock, patch

from models.stop import Stop
from models.route import Route, TransportMode
from services.stop_service import StopService
from services.trip_planner import TripPlanner
from utils.exceptions import StopNotFoundError, NoRouteFoundError

STOPS = [
    Stop("S001", "Sehrekustu", 40.1985, 29.0610, ["T1", "B1"]),
    Stop("S002", "Heykel", 40.1828, 29.0617, ["T1"]),
    Stop("S003", "Kulturpark", 40.1955, 29.0480, ["T1", "B1"]),
    Stop("S005", "Acemler", 40.2050, 28.9900, ["M1", "B1"]),
]
ROUTES = [
    Route("T1", "Sehrekustu - Heykel", TransportMode.TRAM, ["S001", "S003", "S002"]),
    Route("B1", "Kulturpark - Acemler", TransportMode.BUS, ["S003", "S001", "S005"]),
]


def _mock_planner():
    planner = TripPlanner()
    planner._stop_repo = MagicMock()
    planner._route_repo = MagicMock()
    planner._stop_repo.get_all.return_value = STOPS
    planner._route_repo.get_all.return_value = ROUTES
    stop_map = {s.id: s for s in STOPS}
    planner._stop_repo.get_by_id.side_effect = lambda sid: stop_map.get(sid)
    return planner


def test_plan_direct_route():
    planner = _mock_planner()
    trip = planner.plan("S001", "S002")
    assert trip.destination_stop_id == "S002"
    assert len(trip.steps) >= 1


def test_plan_same_stop():
    planner = _mock_planner()
    trip = planner.plan("S001", "S001")
    assert trip.steps == []


def test_plan_no_route():
    planner = _mock_planner()
    # S004 hicbir hatta yok
    planner._stop_repo.get_by_id.side_effect = lambda sid: (
        Stop("S004", "X", 0, 0) if sid == "S004" else {s.id: s for s in STOPS}.get(sid)
    )
    with pytest.raises(NoRouteFoundError):
        planner.plan("S001", "S004")


def test_plan_stop_not_found():
    planner = _mock_planner()
    planner._stop_repo.get_by_id.return_value = None
    with pytest.raises(StopNotFoundError):
        planner.plan("XXXX", "S002")
