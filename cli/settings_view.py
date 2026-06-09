"""Ayarlar ekrani."""
from __future__ import annotations

from services.preference_service import PreferenceService
from utils.exceptions import BursaTransitError


class SettingsView:
    def __init__(self):
        self._pref_svc = PreferenceService()

    def show(self):
        prefs = self._pref_svc.get_prefs()
        print("\n   Ayarlar")
        print(f"  Dil    : {prefs.language}")
        print(f"  Premium: {'Evet' if prefs.is_premium else 'Hayir'}")
        favs = prefs.favorite_stop_ids
        print(f"  Favori duraklar: {', '.join(favs) if favs else '(yok)'}\n")

        print("  [1] Dil degistir")
        print("  [2] Favori durak ekle")
        print("  [3] Favori durak cikar")
        print("  [0] Geri\n")
        choice = input("  Seciminiz: ").strip()

        if choice == "1":
            lang = input("  Dil kodu (tr/en): ").strip().lower()
            try:
                self._pref_svc.set_language(lang)
                print(f"  [OK]  Dil '{lang}' olarak ayarlandi.\n")
            except (BursaTransitError, ValueError) as e:
                print(f"  [!]  {e}\n")

        elif choice == "2":
            sid = input("  Durak ID: ").strip().upper()
            try:
                self._pref_svc.add_favorite(sid)
                print(f"  [OK]  {sid} favorilere eklendi.\n")
            except (BursaTransitError, ValueError) as e:
                print(f"  [!]  {e}\n")

        elif choice == "3":
            sid = input("  Durak ID: ").strip().upper()
            self._pref_svc.remove_favorite(sid)
            print(f"  [OK]  {sid} favorilerden cikarildi.\n")
