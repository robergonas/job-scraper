import requests
import os

TOKEN = os.getenv('TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def test():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": "✅ ¡Hola! Si lees esto, tu bot de Telegram está bien configurado."}
    r = requests.post(url, data=payload)
    print(r.json())

if __name__ == "__main__":
    test()
