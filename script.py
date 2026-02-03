import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Stack técnico: Buscamos .NET con Angular y bases de datos
TECH_STACK = ".net angular (sql OR oracle)"

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML", "disable_web_page_preview": False}
    requests.post(url, data=payload)

def buscar_metabuscadores():
    """Busca en Indeed y LinkedIn usando Google para evitar bloqueos"""
    # Buscamos específicamente en Indeed y LinkedIn ofertas remotas en Perú
    queries = [
        f'site:pe.indeed.com "{TECH_STACK}" remoto',
        f'site:bumeran.com.pe ".net" "angular" "Oracle" "Sql Server" "js" remoto',
        f'site:linkedin.com/jobs/ "{TECH_STACK}" remoto peru'
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
                # Filtramos links reales de Indeed o LinkedIn
                if "indeed.com/viewjob" in href or "linkedin.com/jobs/view" in href:
                    clean_url = href.replace("/url?q=", "").split("&")[0]
                    sitio = "Indeed" if "indeed" in clean_url else "LinkedIn"
                    
                    msg = f"🌟 <b>Nueva vacante en {sitio}</b>\n\n🔗 <a href='{clean_url}'>Abrir oferta</a>"
                    enviar_telegram(msg)
                    encontrados += 1
                    if encontrados >= 5: break # Límite para evitar spam
        except Exception as e:
            print(f"Error buscando en metabuscadores: {e}")
            
    return encontrados

def analizar_laborum():
    url = "https://www.bumeran.com.pe/search-jobs?q=.net+angular"
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
                # Filtro flexible: Tecnologías y Remoto
                if any(t in texto for t in [".net", "angular", "sql", "oracle"]) and \
                   any(r in texto for r in ["remoto", "teletrabajo", "hibrido"]):
                    full_link = "https://www.laborum.pe" + link
                    msg = f"🏢 <b>Vacante en Laborum</b>\n📌 {o.get_text().strip()[:80]}\n🔗 <a href='{full_link}'>Postular</a>"
                    enviar_telegram(msg)
                    encontrados += 1
        return encontrados
    except:
        return 0

if __name__ == "__main__":
    print("Iniciando búsqueda global (Laborum + Indeed + LinkedIn)...")
    l = analizar_laborum()
    m = buscar_metabuscadores()
    
    if (l + m) == 0:
        enviar_telegram("🤖 <b>Reporte:</b> Búsqueda finalizada. Sin vacantes nuevas con este stack hoy.")
