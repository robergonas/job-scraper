import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML", "disable_web_page_preview": True}
    requests.post(url, data=payload)

def buscar_legal_y_eventos():
    # Queries específicas: 
    # 1. Prácticas legales en Lima
    # 2. Trabajos de medio tiempo (Cineplanet, Starbucks, Retail, Eventos)
    queries = [
        'site:pe.indeed.com "practicante de derecho" "lima" "pre profesional"',
        'site:computrabajo.com.pe "estudiante de derecho" "medio tiempo"',
        'site:laborum.pe "part time" "sin experiencia" "lima"'
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    encontrados = 0

    for q in queries:
        query_encoded = urllib.parse.quote(q)
        url = f"https://www.google.com/search?q={query_encoded}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for l in links:
                href = l['href']
                if "http" in href and not "google" in href:
                    clean_url = href.replace("/url?q=", "").split("&")[0]
                    if any(site in clean_url for site in ["indeed", "laborum", "computrabajo"]):
                        msg = f"⚖️ <b>Oportunidad Estudiante / Eventos</b>\n\n🔗 <a href='{clean_url}'>Ver vacante disponible</a>"
                        enviar_telegram(msg)
                        encontrados += 1
                        if encontrados >= 3: break 
        except:
            continue
    return encontrados

if __name__ == "__main__":
    print("Iniciando búsqueda para perfil estudiante...")
    total = buscar_legal_y_eventos()
    if total == 0:
        enviar_telegram("⚖️ <b>Reporte Derecho:</b> Sin nuevas vacantes de medio tiempo hoy.")
