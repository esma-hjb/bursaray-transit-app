"""Repository testleri - gecici dosyalarla izole calisir."""

import pytest
from repositories.base_repository import BaseRepository
from repositories.stop_repository import StopRepository
from repositories.route_repository import RouteRepository


def test_stop_repo_get_all(tmp_stops, monkeypatch):
    monkeypatch.setattr(
        "repositories.stop_repository.StopRepository.file_path", tmp_stops
    )
    repo = StopRepository()
    stops = repo.get_all()
    assert len(stops) == 4
    assert stops[0].id == "S001"


def test_stop_repo_get_by_id(tmp_stops, monkeypatch):
    monkeypatch.setattr(
        "repositories.stop_repository.StopRepository.file_path", tmp_stops
    )
    repo = StopRepository()
    stop = repo.get_by_id("S002")
    assert stop is not None
    assert stop.name == "Heykel"


def test_stop_repo_missing_id(tmp_stops, monkeypatch):
    monkeypatch.setattr(
        "repositories.stop_repository.StopRepository.file_path", tmp_stops
    )
    repo = StopRepository()
    assert repo.get_by_id("XXXX") is None


def test_route_repo_get_by_stop(tmp_routes, monkeypatch):
    monkeypatch.setattr(
        "repositories.route_repository.RouteRepository.file_path", tmp_routes
    )
    repo = RouteRepository()
    routes = repo.get_by_stop("S001")
    route_ids = [r.id for r in routes]
    assert "T1" in route_ids
    assert "B1" in route_ids
