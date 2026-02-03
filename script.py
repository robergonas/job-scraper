import requests
from bs4 import BeautifulSoup
import os
import urllib.parse

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def buscar_especifico_bumeran():
    """Busca directamente en el listado de Bumeran simulando un navegador real"""
    # Buscamos .NET y Remoto por separado para ampliar el radar
    url = "https://www.bumeran.com.pe/empleos-busqueda-.net-remoto.html"
    
    # User-Agent más robusto para saltar bloqueos
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9"
    }

    try:
        res = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # Bumeran guarda las ofertas en etiquetas 'a' con un ID de aviso
        ofertas = soup.find_all('a', href=True)
        encontrados = 0

        for o in ofertas:
            link = o['href']
            # Identificamos el patrón de links de empleo en Bumeran
            if "/empleos/" in link and "-11" in link: # El '-11' es típico de sus IDs
                titulo = o.get_text().lower()
                
                # CRITERIO FLEXIBLE: Si dice .NET y es remoto, avisar sí o sí.
                if ".net" in titulo:
                    full_link = "https://www.bumeran.com.pe" + link if not link.startswith("http") else link
                    msg = f"🔥 <b>¡DETECTADA EN BUMERAN!</b>\n\n📌 {titulo.upper()}\n🔗 <a href='{full_link}'>Postular ahora mismo</a>"
                    enviar_telegram(msg)
                    encontrados += 1
                    if encontrados >= 3: break
        return encontrados
    except Exception as e:
        print(f"Error en Bumeran directo: {e}")
        return 0

if __name__ == "__main__":
    # Ejecutamos la búsqueda directa y luego la de Google como respaldo
    print("Buscando en Bumeran...")
    b = buscar_especifico_bumeran()
    
    # Mensaje de log para ti en la consola de GitHub
    print(f"Búsqueda finalizada. {b} ofertas encontradas directamente.")
