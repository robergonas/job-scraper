import requests
from bs4 import BeautifulSoup

# CONFIGURACIÓN (Luego configuraremos esto de forma segura)
TOKEN = "TU_TOKEN_AQUI"
CHAT_ID = "TU_CHAT_ID_AQUI"
URL_BUSQUEDA = "AQUI_VA_LA_URL_DE_LA_BOLSA"

def buscar_empleos():
    # 1. Entramos a la web
    headers = {'User-Agent': 'Mozilla/5.0'}
    respuesta = requests.get(URL_BUSQUEDA, headers=headers)
    sopa = BeautifulSoup(respuesta.text, 'html.parser')
    
    # 2. Buscamos todas las ofertas (esto varía según la web)
    # Por ahora, buscaremos etiquetas de enlaces <a> que tengan texto
    ofertas = sopa.find_all('a')
    
    mensajes_enviados = 0

    for oferta in ofertas:
        texto = oferta.text.lower()
        link = oferta.get('href')

        # 3. FILTRO: ¿Dice Netflix y Remoto?
        if "netflix" in texto and (".net" in texto or "remote" in texto):
            mensaje = f"🚀 <b>¡Nueva Oferta Encontrada!</b>\n\n📌 {oferta.text}\n🔗 {link}"
            enviar_telegram(mensaje)
            mensajes_enviados += 1
            
    if mensajes_enviados == 0:
        print("No se encontraron ofertas hoy.")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
    requests.post(url, data=payload)

if __name__ == "__main__":
    buscar_empleos()
