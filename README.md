# YouTube Transcript Fetcher

![YouTube Icon](https://img.shields.io/badge/YouTube-Altyazı%20Çekici-red?style=flat&logo=youtube)  
Tez projesi: YouTube videolarından otomatik altyazı (TR/EN) çeken web app. Flask tabanlı prototip.

## Özellikler
- Video ID ile altyazı çek (TR yoksa EN auto-generated).
- Modern Bootstrap UI: Responsive, loading animasyonu.
- Kopyala butonu, tam metin gösterimi.
- Demo: [Yerel: http://127.0.0.1:5000](http://127.0.0.1:5000) (çalıştırınca).

## Kurulum
1. Python 3.8+ yükle.
2. Sanal ortam oluştur: `python -m venv venv` ve `source venv/bin/activate` (Linux/Mac).
3. Paketleri yükle: `pip install -r requirements.txt`.
4. Çalıştır: `python app.py`.
5. Tarayıcıda aç: http://127.0.0.1:5000.

### Test
- Video ID: `jjrTOzJ9cFY` (Türkçe video, EN auto altyazı çeker).
- Beklenen: Tam transcript metni.

## Deployment
- **Heroku/Render**: Ücretsiz deploy (Procfile ekle: `web: python app.py`).
- **Vercel**: Flask için adapter kullan.

## Gelecek Özellikler
- Özetleme entegrasyonu (Hugging Face).
- TXT/PDF export.
- Türkçe çeviri.

## Lisans
MIT License. Yazar: Burak [GitHub: @kullanicin].

![Stars](https://img.shields.io/github/stars/kullanicin/youtube-transcript-fetcher?style=social)