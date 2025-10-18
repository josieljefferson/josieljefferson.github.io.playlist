from flask import Flask, send_file
import requests
import gzip
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h2>🎬 Servidor IPTV Público + EPG Local</h2>
    <ul>
      <li><a href="/playlists.m3u8">Baixar Playlist M3U</a></li>
      <li><a href="/epg.xml">Ver Guia de Programação (EPG XML)</a></li>
    </ul>
    """

@app.route('/playlists.m3u8')
def playlist():
    return send_file('channels.m3u', mimetype='audio/x-mpegurl')

@app.route('/epg.xml')
def epg():
    # Baixa e combina EPGs dinamicamente
    urls = [
        "https://m3u4u.com/epg/jq2zy9epr3bwxmgwyxr5",
        "https://m3u4u.com/epg/3wk1y24kx7uzdevxygz7",
        "https://m3u4u.com/epg/782dyqdrqkh1xegen4zp",
        "https://www.open-epg.com/files/brazil1.xml.gz",
        "https://www.open-epg.com/files/brazil2.xml.gz",
        "https://www.open-epg.com/files/brazil3.xml.gz",
        "https://www.open-epg.com/files/brazil4.xml.gz",
        "https://www.open-epg.com/files/portugal1.xml.gz",
        "https://www.open-epg.com/files/portugal2.xml.gz",
        "https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz",
        "https://epgshare01.online/epgshare01/epg_ripper_PT1.xml.gz"
    ]

    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'
    for url in urls:
        try:
            r = requests.get(url, timeout=15)
            if url.endswith(".gz"):
                xml_part = gzip.GzipFile(fileobj=BytesIO(r.content)).read().decode("utf-8", errors="ignore")
            else:
                xml_part = r.text
            xml_part = xml_part.replace('<?xml version="1.0" encoding="UTF-8"?>', '').replace('<tv>', '').replace('</tv>', '')
            xml += xml_part
        except Exception as e:
            print(f"Erro em {url}: {e}")
    xml += "</tv>"
    return xml, 200, {'Content-Type': 'application/xml; charset=utf-8'}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)