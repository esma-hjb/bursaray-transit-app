"""JSON kalicilik katmani.

Diskteki JSON dosyalarini okuyup yazmak icin basit yardimci fonksiyonlar.
Tum repository'ler veriyi okurken/yazarken buradaki fonksiyonlari kullanir.
"""
from __future__ import annotations

import json
from pathlib import Path


def read_json(path, default=None):
    """Bir JSON dosyasini okur ve icindeki veriyi (liste/sozluk) dondurur.

    Dosya yoksa VEYA bos ise hata vermek yerine 'default' degerini dondurur.
    Boylece program ilk calistiginda dosya henuz yoksa/bossa cokmeyiz.
    """
    p = Path(path)
    if not p.exists():
        return default
    text = p.read_text(encoding="utf-8").strip()
    if not text:
        return default
    return json.loads(text)


def write_json(path, data):
    """Veriyi (liste/sozluk) bir JSON dosyasina yazar.

    Klasor yoksa olusturur. ensure_ascii=False sayesinde Turkce karakterler
    dosyada okunabilir sekilde saklanir; indent=2 ile duzgun girintili yazilir.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)