"""Tum liste-tabanli repository'ler icin ortak temel sinif.

Bir repository, belirli bir model turunu (orn. Stop) JSON dosyasindan
okuyup nesneye ceviren ve nesneleri tekrar dosyaya yazan katmandir.
Boylece servis/CLI katmani dosya islemleriyle ugrasmaz; sadece nesnelerle calisir.
"""

from __future__ import annotations

from storage.json_storage import read_json, write_json


class BaseRepository:
    """JSON dosyasindan model nesneleri okuyup yazan temel repository.

    Alt siniflar su iki alani tanimlamalidir:
        file_path: Verinin tutuldugu JSON dosyasinin yolu (config'ten).
        model_cls: Kullanilacak model sinifi (from_dict/to_dict metotlu).
    """

    file_path = None
    model_cls = None

    def __init__(self):
        if self.file_path is None or self.model_cls is None:
            raise NotImplementedError(
                "Alt sinif 'file_path' ve 'model_cls' tanimlamalidir."
            )

    def get_all(self):
        """Dosyadaki tum kayitlari model nesnesi listesi olarak dondurur."""
        raw = read_json(self.file_path, default=[])
        return [self.model_cls.from_dict(item) for item in raw]

    def get_by_id(self, item_id):
        """Verilen id'ye sahip nesneyi dondurur; bulamazsa None."""
        for obj in self.get_all():
            if obj.id == item_id:
                return obj
        return None

    def save_all(self, items):
        """Verilen nesne listesini dosyaya yazar (mevcut veriyi degistirir)."""
        write_json(self.file_path, [obj.to_dict() for obj in items])
