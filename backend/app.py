from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp, os

app = Flask(__name__)
CORS(app)

@app.route('/convert')
def convert():
    url = request.args.get('url')
    try:
        with yt_dlp.YoutubeDL({'format': 'bestaudio/best', 'quiet': True, 'cookiefile': 'cookies.txt'}) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            audio_url = next((f['url'] for f in reversed(formats) if f.get('acodec') != 'none' and f.get('vcodec') == 'none'), info.get('url'))
            return jsonify({'success': True, 'title': info['title'], 'thumbnail': info.get('thumbnail'), 'audio_url': audio_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def health():
    return jsonify({'status': 'running'})

if __name__ == '__main__':
    import os
port = int(os.environ.get('PORT', 5000))
app.run(host='0.0.0.0', port=port)