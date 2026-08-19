!pip install requests beautifulsoup4

imporimport time
from bs4 import BeautifulSoup
imporimport requests

DISCORD_WEBHOOK = "https://discord.com/api/webhooks/1539336819727016016/oZx0kn0GzyCxgVu1rooRAo0wXxUxCy7z1Yfx9pY800aS30mWHJeqtZyxxKi9VAj4-Xez"
URL = "https://amzn.eu/d/06FiKIlU"
PREZZO_SOGLIA = 9999.0  # Messa alta per inviare SEMPRE la notifica di test

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (iPad; CPU OS 17_0 like Mac OS X) AppleWebKit/605.1.15"
        " (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    ),
    "Accept-Language": "it-IT,it;q=0.9",
}


def invia_notifica_discord(messaggio):
  payload = {"content": messaggio}
  requests.post(DISCORD_WEBHOOK, json=payload)


def controlla_prezzo():
  try:
    risposta = requests.get(URL, headers=HEADERS)
    soup = BeautifulSoup(risposta.content, "html.parser")
    prezzo_tag = soup.find("span", {"class": "a-offscreen"})

    if prezzo_tag:
      testo = prezzo_tag.get_text()
      pulito = testo.replace("€", "").replace(".", "").replace(",", ".").strip()
      prezzo = float(pulito)
      print(f"Prezzo trovato: {prezzo}€")

      if prezzo <= PREZZO_SOGLIA:
        invia_notifica_discord(
            f"🔥**SCONTO AMAZON!!!**\nIl prezzo è sceso a **{prezzo}€**!\n👉 {URL}"
        )
        print("Notifica inviata su Discord!")
      else:
        print("Prezzo sopra la soglia.")
    else:
      print("Impossibile trovare l'elemento del prezzo su Amazon")
  except Exception as e:
    print(f"Errore durante il controllo: {e}")


# Chiamata indispensabile per eseguire il codice
controlla_prezzo()
