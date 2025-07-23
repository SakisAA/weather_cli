import requests
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

# Φόρτωσε τις μεταβλητές από το .env
load_dotenv()

# Πάρε το API key από τις μεταβλητές περιβάλλοντος
def get_weather_data(city):
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise ValueError("Το API key δεν βρέθηκε! Βεβαιώσου ότι υπάρχει στο .env")

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "el"
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 401:
        raise Exception("❌ Σφάλμα: Invalid API key. Ελέγξτε το API key σας.")
    elif response.status_code == 404:
        raise Exception("❌ Σφάλμα: Η πόλη δεν βρέθηκε.")
    elif response.status_code != 200:
        raise Exception(f"❌ Άγνωστο σφάλμα: {response.status_code}")

    return response.json()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Χρήση: python weather.py <πόλη>")
        sys.exit(1)

    city = sys.argv[1]
    try:
        data = get_weather_data(city)
        print(f"🌤 Καιρός στην πόλη {city}: {data['weather'][0]['description']}")
        print(f"🌡 Θερμοκρασία: {data['main']['temp']}°C")
        print(f"💨 Άνεμος: {data['wind']['speed']} m/s")
        print(f"💧 Υγρασία: {data['main']['humidity']}%")
        print(f"🌅 Ανατολή: {datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')}")
    except Exception as e:
        print(str(e))

