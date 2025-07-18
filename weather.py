import requests
import sys
import os
from dotenv import load_dotenv

# Φόρτωσε τις μεταβλητές από το .env
load_dotenv()

# Πάρε το API key από τις μεταβλητές περιβάλλοντος
API_KEY = os.getenv("API_KEY")

if not API_KEY:
    raise ValueError("Το API key δεν βρέθηκε! Βεβαιώσου ότι υπάρχει στο .env")

# Παράδειγμα χρήσης:
print(f"Το API key είναι: {API_KEY}")

BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

if len(sys.argv) < 2:
    print("Χρήση: python weather.py <πόλη>")
    sys.exit(1)

city = sys.argv[1]
params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric",
    "lang": "el"
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 401:
    print("❌ Σφάλμα: Invalid API key. Ελέγξτε το API key σας.")
elif response.status_code == 404:
    print("❌ Σφάλμα: Η πόλη δεν βρέθηκε.")
elif response.status_code != 200:
    print(f"❌ Άγνωστο σφάλμα: {response.status_code}")
else:
    data = response.json()
    print(f"🌤 Καιρός στην πόλη {city}: {data['weather'][0]['description']}")
    print(f"🌡 Θερμοκρασία: {data['main']['temp']}°C")
    print(f"💨 Άνεμος: {data['wind']['speed']} m/s")

print(response.url)