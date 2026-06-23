"""Kullanici tercihleri (UserPrefs) erisim katmani.

Diger repository'lerden farkli olarak burada bir LISTE degil, TEK bir
kullanici tercih nesnesi saklanir (data/user_data.json). Bu yuzden
BaseRepository yerine kendi load/save metotlarini yazariz.
"""

from __future__ import annotations

from config import USER_DATA_FILE
from models.user_prefs import UserPrefs
from storage.json_storage import read_json, write_json


class UserRepository:
    """Kullanici tercihlerini tek bir JSON dosyasinda saklar."""

    file_path = USER_DATA_FILE

    def load(self):
        """Tercihleri dosyadan okur. Dosya yoksa varsayilan tercihleri dondurur."""
        data = read_json(self.file_path, default=None)
        if not data:
            return UserPrefs()
        return UserPrefs.from_dict(data)

    def save(self, prefs):
        """Verilen UserPrefs nesnesini dosyaya yazar."""
        write_json(self.file_path, prefs.to_dict())
