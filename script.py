import requests
from bs4 import BeautifulSoup
import os

# Configuración desde GitHub Secrets
TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# URL de búsqueda en Laborum (Filtramos por Netflix)
URL = "https://www.laborum.pe/search-jobs?q=.Net"

def buscar_empleos():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(URL, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # En Laborum, las ofertas suelen estar en etiquetas <a> que contienen "/job/"
        ofertas = soup.find_all('a', href=True)
        encontrados = []

        for o in ofertas:
            link = o['href']
            # Filtramos que sea una oferta real y contenga las palabras clave
            if "/job/" in link:
                texto = o.get_text().lower()
                # Buscamos 'netflix' y 'remoto' en el texto de la oferta
                if "netflix" in texto or "remoto" in texto:
                    titulo = o.get_text().strip()
                    url_completa = f"https://www.laborum.pe{link}"
                    if url_completa not in encontrados:
                        encontrados.append(url_completa)
                        enviar_telegram(f"🎯 <b>¡Posible vacante!</b>\n\n📌 {titulo}\n🔗 {url_completa}")

        if not encontrados:
            print("No hubo novedades hoy.")

    except Exception as e:
        print(f"Error: {e}")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
    requests.post(url, data=payload)

if __name__ == "__main__":
    buscar_empleos()
