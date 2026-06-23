"""Kullanici tercihleri is mantigi servisi."""

from __future__ import annotations

from repositories.user_repository import UserRepository
from utils.exceptions import StopNotFoundError
from utils.validators import validate_language, validate_stop_id


class PreferenceService:
    """Kullanici tercihlerini yonetir (dil, favoriler, premium)."""

    def __init__(self):
        self._user_repo = UserRepository()

    def get_prefs(self):
        """Mevcut kullanici tercihlerini dondurur."""
        return self._user_repo.load()

    def set_language(self, lang: str):
        """Arayuz dilini degistirir."""
        validate_language(lang)
        prefs = self._user_repo.load()
        prefs.language = lang
        self._user_repo.save(prefs)

    def add_favorite(self, stop_id: str):
        """Duragi favorilere ekler (zaten varsa atlar)."""
        validate_stop_id(stop_id)
        prefs = self._user_repo.load()
        if stop_id not in prefs.favorite_stop_ids:
            prefs.favorite_stop_ids.append(stop_id)
            self._user_repo.save(prefs)

    def remove_favorite(self, stop_id: str):
        """Duragi favorilerden cikarir."""
        prefs = self._user_repo.load()
        if stop_id in prefs.favorite_stop_ids:
            prefs.favorite_stop_ids.remove(stop_id)
            self._user_repo.save(prefs)

    def get_favorites(self):
        """Favori durak ID'lerinin listesini dondurur."""
        return self._user_repo.load().favorite_stop_ids
