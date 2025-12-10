# YouTube Altyazı Çekici Web App - Güzel UI Versiyonu (Bootstrap)
# Özellikler: Modern tasarım, loading bar, responsive.
# Kurulum: pip install flask youtube-transcript-api (venv'de).
# Çalıştır: python app.py → http://127.0.0.1:5000/

from flask import Flask, request, render_template_string
from youtube_transcript_api import YouTubeTranscriptApi
import time  # Loading simülasyonu için (gerçekte kaldırmayabilirsin)

app = Flask(__name__)

# HTML Template (Bootstrap + Font Awesome)
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Altyazı Çekici</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" rel="stylesheet">
    <style>
        body { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
        .hero { background: white; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
        .btn-primary { background: #ff0000; border-color: #ff0000; } /* YouTube kırmızı */
        .btn-primary:hover { background: #cc0000; }
        .progress { height: 8px; border-radius: 10px; }
        .transcript { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 10px; max-height: 500px; overflow-y: auto; white-space: pre-wrap; font-family: monospace; }
        .loading { display: none; text-align: center; margin: 20px 0; }
        footer { margin-top: 50px; color: white; text-align: center; }
    </style>
</head>
<body>
    <div class="container py-5">
        <div class="row justify-content-center">
            <div class="col-md-8">
                <div class="hero p-4 p-md-5 text-center">
                    <h1 class="mb-4"><i class="fab fa-youtube text-danger"></i> YouTube Altyazı Çekici</h1>
                    <p class="lead text-muted">Video ID girin, otomatik altyazıyı (TR/EN) çekin. Tez projesi prototipi.</p>
                    
                    <form method="POST" id="form">
                        <div class="mb-3">
                            <label for="video_id" class="form-label"><i class="fas fa-link"></i> YouTube Video ID</label>
                            <input type="text" class="form-control" id="video_id" name="video_id" placeholder="örn: jjrTOzJ9cFY" required>
                            <div class="form-text">URL'den ID'yi kopyalayın: youtube.com/watch?v=ID</div>
                        </div>
                        <button type="submit" class="btn btn-primary btn-lg w-100"><i class="fas fa-download"></i> Altyazıyı Çek!</button>
                    </form>
                    
                    <!-- Loading Spinner -->
                    <div class="loading" id="loading">
                        <div class="spinner-border text-primary" role="status">
                            <span class="visually-hidden">Yükleniyor...</span>
                        </div>
                        <p class="mt-2">Altyazı çekiliyor... (Birkaç saniye)</p>
                        <div class="progress">
                            <div class="progress-bar progress-bar-striped progress-bar-animated" style="width: 100%"></div>
                        </div>
                    </div>
                </div>
                
                {% if transcript %}
                <div class="hero mt-4 p-4">
                    <h2 class="mb-3"><i class="fas fa-file-alt"></i> Çekilen Altyazı ({{ lang }} Dili)</h2>
                    <div class="transcript p-3 mb-3">{{ transcript }}</div>
                    <div class="alert alert-info">
                        <small><i class="fas fa-info-circle"></i> Tam metin ({{ transcript|length }} karakter). Kopyala veya indir. Not: Auto-generated EN kalitesi orta olabilir.</small>
                    </div>
                    <button class="btn btn-outline-secondary" onclick="navigator.clipboard.writeText('{{ transcript }}'); alert('Kopyalandı!')">
                        <i class="fas fa-copy"></i> Kopyala
                    </button>
                </div>
                {% endif %}
                
                {% if error %}
                <div class="alert alert-danger mt-4">
                    <h4><i class="fas fa-exclamation-triangle"></i> Hata!</h4>
                    <p>{{ error }}</p>
                </div>
                {% endif %}
            </div>
        </div>
    </div>
    
    <footer>
        <p>&copy; 2025 Tez Projesi - Burak. <a href="https://github.com/kullanicin/youtube-transcript-fetcher" class="text-white">GitHub Repo</a></p>
    </footer>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        document.getElementById('form').addEventListener('submit', function() {
            document.getElementById('loading').style.display = 'block';
        });
    </script>
</body>
</html>
"""

def get_transcript(video_id, preferred_language='tr'):
    """
    Altyazı çeker (önce TR, yoksa EN).
    """
    languages_to_try = [preferred_language, 'en']
    for lang in languages_to_try:
        try:
            ytt_api = YouTubeTranscriptApi()
            transcript_list = ytt_api.fetch(video_id, languages=[lang])
            text = ' '.join([entry.text for entry in transcript_list])
            return text, lang
        except Exception as e:
            continue
    return None, None

@app.route('/', methods=['GET', 'POST'])
def index():
    transcript = None
    lang = None
    error = None
    
    if request.method == 'POST':
        video_id = request.form['video_id'].strip()
        if not video_id:
            error = "Video ID boş olamaz!"
        else:
            # Kısa delay simüle (gerçek API için kaldır)
            # time.sleep(2)
            transcript_text, fetched_lang = get_transcript(video_id)
            if transcript_text:
                transcript = transcript_text
                lang = fetched_lang
            else:
                error = f"Altyazı çekilemedi (ID: {video_id}). Videoda CC (altyazı) var mı kontrol edin? (TR yoksa EN auto denenir.)"
    
    return render_template_string(HTML_TEMPLATE, 
                                  transcript=transcript, 
                                  lang=lang, 
                                  error=error)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)