from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp, os

app = Flask(__name__)
CORS(app)

@app.route('/convert')
def convert():
    url = request.args.get('url')
    try:
        opts = {
            'quiet': True,
            'cookiefile': 'cookies.txt',
            'format': 'worstaudio/worst',
        }
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=False)
            formats = info.get('formats', [])
            
            # pick any audio format available
            audio = None
            for f in formats:
                if f.get('acodec') != 'none':
                    audio = f
                    break
            
            if not audio:
                audio_url = info.get('url')
            else:
                audio_url = audio.get('url')

            return jsonify({
                'success': True,
                'title': info['title'],
                'thumbnail': info.get('thumbnail'),
                'audio_url': audio_url,
                'duration': info.get('duration')
            })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def health():
    return jsonify({'status': 'running'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)