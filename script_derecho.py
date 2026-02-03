import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

TOKEN = os.getenv('TOKENJCG')
CHAT_ID = os.getenv('CHAT_IDJCG')

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML", "disable_web_page_preview": True}
    requests.post(url, data=payload)

def buscar_legal_y_eventos():
    # Buscamos: Prácticas, Notarías, Procuradores y Part-time genérico
    queries = [
        'site:pe.indeed.com "practicante de derecho" OR "notaria" "lima"',
        'site:computrabajo.com.pe "procurador" OR "asistente legal" "medio tiempo"',
        'site:laborum.pe "part time" "estudiante" "sin experiencia"'
    ]
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    encontrados = 0

    for q in queries:
        query_encoded = urllib.parse.quote(q)
        url = f"https://www.google.com/search?q={query_encoded}"
        try:
            res = requests.get(url, headers=headers, timeout=15)
            soup = BeautifulSoup(res.text, 'html.parser')
            links = soup.find_all('a', href=True)
            
            for l in links:
                href = l['href']
                if "http" in href and not "google" in href:
                    clean_url = href.replace("/url?q=", "").split("&")[0]
                    # Filtro de dominios de confianza
                    if any(site in clean_url for site in ["indeed", "laborum", "computrabajo", "linkedin"]):
                        msg = f"⚖️ <b>Oportunidad Estudiante / Eventos</b>\n\n🔗 <a href='{clean_url}'>Ver vacante disponible</a>"
                        enviar_telegram(msg)
                        encontrados += 1
                        if encontrados >= 3: break 
        except Exception as e:
            print(f"Error en query legal: {e}")
    return encontrados

if __name__ == "__main__":
    print("Iniciando radar legal/estudiante...")
    total = buscar_legal_y_eventos()
    if total == 0:
        enviar_telegram("⚖️ <b>Reporte Derecho:</b> Búsqueda diaria lista. No se hallaron nuevas vacantes hoy.")
    print(f"Proceso finalizado. Encontrados: {total}")
