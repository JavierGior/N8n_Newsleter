import sys
import json
import hashlib
import requests
import trafilatura
from urllib.parse import urlparse

# Configuración de headers para evitar bloqueos (tomado de tu scraper_web.py)
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
}

def clean_url(url):
    """Limpia parámetros de tracking de la URL"""
    try:
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    except:
        return url

def get_content(url):
    clean_link = clean_url(url)
    
    try:
        # 1. Descarga con Trafilatura (intento directo)
        downloaded = trafilatura.fetch_url(clean_link)
        
        # 2. Fallback a Requests si Trafilatura falla (headers custom)
        if not downloaded:
            try:
                resp = requests.get(clean_link, headers=HEADERS, timeout=15, verify=False)
                if resp.status_code == 200:
                    downloaded = resp.text
            except Exception as e:
                return {"status": "error", "message": f"Download failed: {str(e)}"}

        if not downloaded:
            return {"status": "error", "message": "Empty response"}

        # 3. Extracción de contenido limpio
        text = trafilatura.extract(
            downloaded,
            include_comments=False,
            include_tables=True, # Importante para datos financieros
            no_fallback=False,
            include_links=False
        )

        if not text or len(text) < 150: # Filtro de contenido muy corto/error
            return {"status": "skipped", "message": "Content too short or empty"}

        # 4. Generar Hash para deduplicación (MD5 del texto limpio)
        content_hash = hashlib.md5(text.encode('utf-8')).hexdigest()

        return {
            "status": "success",
            "url": clean_link,
            "text": text,
            "content_hash": content_hash,
            "length": len(text)
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    # n8n pasará la URL como primer argumento
    if len(sys.argv) < 2:
        print(json.dumps({"status": "error", "message": "No URL provided"}))
        sys.exit(1)
        
    target_url = sys.argv[1]
    result = get_content(target_url)
    
    # IMPORTANTE: Imprimimos SOLO el JSON para que n8n lo lea
    print(json.dumps(result))