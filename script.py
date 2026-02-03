import requests
from bs4 import BeautifulSoup
import os

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
    r = requests.post(url, data=payload)
    print(f"DEBUG Telegram: Enviado a {CHAT_ID}. Status: {r.status_code}")
    return r.status_code

def buscar_test():
    # Buscamos algo genérico en Laborum para forzar resultados
    url = "https://www.laborum.pe/search-jobs?q=desarrollador"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        # Buscamos cualquier link de trabajo
        ofertas = soup.find_all('a', href=True)
        
        contador = 0
        for o in ofertas:
            if "/job/" in o['href'] and contador < 3:
                link = "https://www.laborum.pe" + o['href']
                enviar_telegram(f"🔍 <b>Oferta encontrada:</b>\n{link}")
                contador += 1
        
        return contador
    except Exception as e:
        print(f"Error: {e}")
        return 0

if __name__ == "__main__":
    print("Iniciando prueba forzada...")
    enviar_telegram("🚀 El script ha iniciado correctamente.")
    encontrados = buscar_test()
    enviar_telegram(f"🏁 Prueba finalizada. Ofertas enviadas: {encontrados}")
