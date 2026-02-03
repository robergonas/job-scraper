import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Stack técnico y modalidad
TECH_STACK = ".net angular (sql OR oracle) (javascript OR typescript)"
REMOTOS = ["remoto", "teletrabajo", "home office"]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML", "disable_web_page_preview": False}
    requests.post(url, data=payload)

def buscar_en_google():
    """Busca ofertas recientes indexadas por Google en LinkedIn y portales corporativos"""
    # Buscamos ofertas de los últimos 7 días con tu stack
    query = f'site:linkedin.com/jobs/ "{TECH_STACK}" remoto peru'
    query_encoded = urllib.parse.quote(query)
    url = f"https://www.google.com/search?q={query_encoded}"
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Buscamos los links de resultados de Google
        links = soup.find_all('a', href=True)
        
        encontrados = 0
        for l in links:
            href = l['href']
            if "/jobs/view/" in href or "linkedin.com/jobs" in href:
                # Extraer la URL limpia de LinkedIn
                clean_url = href.split("&")[0].replace("/url?q=", "")
                msg = f"🌟 <b>Oportunidad en LinkedIn (vía Google)</b>\n\n🔗 <a href='{clean_url}'>Ver vacante</a>"
                enviar_telegram(msg)
                encontrados += 1
                if encontrados >= 3: break
        return encontrados
    except:
        return 0

def analizar_laborum():
    url = "https://www.laborum.pe/search-jobs?q=.net+angular+sql"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        ofertas = soup.find_all('a', href=True)
        
        encontrados = 0
        for o in ofertas:
            link = o['href']
            if "/job/" in link:
                texto = o.get_text().lower()
                if any(tech in texto for tech in [".net", "angular", "sql"]) and any(r in texto for r in REMOTOS):
                    full_link = "https://www.laborum.pe" + link
                    msg = f"🏢 <b>Vacante en Laborum</b>\n📌 {o.get_text().strip()[:80]}\n🔗 <a href='{full_link}'>Postular</a>"
                    enviar_telegram(msg)
                    encontrados += 1
        return encontrados
    except:
        return 0

if __name__ == "__main__":
    print("Iniciando búsqueda avanzada...")
    l = analizar_laborum()
    g = buscar_en_google()
    
    if (l + g) == 0:
        enviar_telegram("☕ <b>Reporte:</b> No se hallaron nuevas vacantes hoy. ¡Buen día!")
