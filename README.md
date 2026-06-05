# Bursaray Transit App

Bursa toplu taşıma (otobüs + metro + tramvay) için durak sorgulama,
canlı araç takibi ve rota planlama uygulaması.

## Özellikler
- Yakındaki durakları bulma (konuma göre)
- Hat/durak detayları ve tahmini varış (ETA)
- Origin → Destination rota planlama (çoklu-mod)
- (İleride) Canlı araç takibi, premium, AI kamera ile hat tanıma

## Mimari
Katmanlı yapı: `models → repositories/storage → services → cli`
- `models/`      : Veri modelleri (Stop, Route, Trip, UserPrefs)
- `repositories/`: Veri erişim katmanı
- `storage/`     : JSON kalıcılık
- `services/`    : İş mantığı (yakın durak, rota planlama)
- `cli/`         : Komut satırı arayüzü
- `data/`        : Tohum (seed) veri

## Kurulum
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Çalıştırma
```bash
python main.py
```

## Test
```bash
pytest
```

## Durum
Geliştirme aşamasında (flowchart'a göre fazlar halinde ilerleniyor).
