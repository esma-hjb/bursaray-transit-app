"""UserPrefs (Kullanıcı tercihleri) veri modeli.

Kullanıcının uygulama tercihlerini temsil eder: dil, premium üyelik durumu
ve favori duraklar. Bu veri çalışma anında üretilir ve config.USER_DATA_FILE
dosyasında saklanır (flowchart'taki "Onboarding / Language & preferences" adımı).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from config import DEFAULT_LANGUAGE


@dataclass
class UserPrefs:
    """Kullanıcının tercihleri.

    Alanlar:
        language: Arayüz dili (örn. "tr" veya "en").
        is_premium: Kullanıcı premium üye mi? (flowchart'taki "Premium user?").
        favorite_stop_ids: Kullanıcının favori durak kimlikleri.
    """

    language: str = DEFAULT_LANGUAGE
    is_premium: bool = False
    favorite_stop_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Modeli JSON'a yazılabilir bir sözlüğe çevirir."""
        return {
            "language": self.language,
            "is_premium": self.is_premium,
            "favorite_stop_ids": self.favorite_stop_ids,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserPrefs":
        """JSON'dan okunan bir sözlükten UserPrefs nesnesi oluşturur."""
        return cls(
            language=data.get("language", DEFAULT_LANGUAGE),
            is_premium=bool(data.get("is_premium", False)),
            favorite_stop_ids=list(data.get("favorite_stop_ids", [])),
        )
