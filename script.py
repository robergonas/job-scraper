import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

# Tu stack tecnológico ampliado
KEYWORDS = [".net", "sql", "oracle", "angular", "javascript", "typescript", "c#", "ts", "js"]
# Palabras clave para modalidad flexible
REMOTOS = ["remoto", "remote", "teletrabajo", "home office", "hibrido", "hybrid"]

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
    requests.post(url, data=payload)

def analizar_laborum():
    # Buscamos con términos base para obtener una lista amplia
    terminos_busqueda = ".net+angular+javascript"
    url = f"https://www.laborum.pe/search-jobs?q={terminos_busqueda}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        ofertas = soup.find_all('a', href=True)
        
        encontrados = 0
        vistos = set() # Para no repetir ofertas

        for o in ofertas:
            link = o['href']
            if "/job/" in link and link not in vistos:
                vistos.add(link)
                texto_oferta = o.get_text().lower()
                
                # LÓGICA DE FILTRADO
                # 1. ¿Tiene alguna de tus tecnologías?
                tiene_tech = any(tech in texto_oferta for tech in KEYWORDS)
                
                # 2. ¿Es remoto o híbrido?
                es_remoto = any(rem in texto_oferta for rem in REMOTOS)

                if tiene_tech and es_remoto:
                    full_link = "https://www.laborum.pe" + link
                    # Formateamos el mensaje para que se vea profesional
                    msg = (
                        f"🎯 <b>Oportunidad Detectada</b>\n"
                        f"━━━━━━━━━━━━━━━━━━\n"
                        f"📝 <b>Posición:</b> {o.get_text().strip()[:80]}...\n"
                        f"🌐 <b>Modalidad:</b> Remoto / Híbrido\n"
                        f"🔗 <a href='{full_link}'>Ver detalles de la oferta</a>"
                    )
                    enviar_telegram(msg)
                    encontrados += 1
                    
        return encontrados
    except Exception as e:
        print(f"Error en la búsqueda: {e}")
        return 0

if __name__ == "__main__":
    print("Iniciando buscador de perfiles Senior...")
    total = analizar_laborum()
    if total > 0:
        print(f"Se enviaron {total} alertas.")
    else:
        # Enviamos una confirmación una vez al día para saber que el bot trabajó
        enviar_telegram("🤖 <b>Reporte Diario:</b> Búsqueda completada. No se hallaron nuevas vacantes con el perfil exacto hoy.")
