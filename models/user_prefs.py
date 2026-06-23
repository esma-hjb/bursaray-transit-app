"""UserPrefs (Kullanici tercihleri) veri modeli.

Kullanicinin uygulama tercihlerini temsil eder: dil, premium uyelik durumu
ve favori duraklar. Bu veri calisma aninda uretilir ve config.USER_DATA_FILE
dosyasinda saklanir (flowchart'taki "Onboarding / Language & preferences" adimi).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from config import DEFAULT_LANGUAGE


@dataclass
class UserPrefs:
    """Kullanicinin tercihleri.

    Alanlar:
        language: Arayuz dili (orn. "tr" veya "en").
        is_premium: Kullanici premium uye mi? (flowchart'taki "Premium user?").
        favorite_stop_ids: Kullanicinin favori durak kimlikleri.
    """

    language: str = DEFAULT_LANGUAGE
    is_premium: bool = False
    favorite_stop_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Modeli JSON'a yazilabilir bir sozluge cevirir."""
        return {
            "language": self.language,
            "is_premium": self.is_premium,
            "favorite_stop_ids": self.favorite_stop_ids,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "UserPrefs":
        """JSON'dan okunan bir sozlukten UserPrefs nesnesi olusturur."""
        return cls(
            language=data.get("language", DEFAULT_LANGUAGE),
            is_premium=bool(data.get("is_premium", False)),
            favorite_stop_ids=list(data.get("favorite_stop_ids", [])),
        )
