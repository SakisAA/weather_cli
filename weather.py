import requests
import sys
import os
from dotenv import load_dotenv
from datetime import datetime

# Φορτώνουμε τις μεταβλητές περιβάλλοντος από το αρχείο .env
# (πρέπει να υπάρχει API_KEY μέσα σε αυτό)
load_dotenv()

def get_weather_data(city):
    """
    Αντλεί δεδομένα καιρού από το OpenWeather API για την πόλη που δίνεται.

    Args:
        city (str): Όνομα της πόλης (π.χ. "Athens").

    Returns:
        dict: Λεξικό με τα δεδομένα καιρού όπως τα επιστρέφει το API.

    Raises:
        ValueError: Αν το API_KEY δεν βρεθεί στις μεταβλητές περιβάλλοντος.
        Exception: Αν το API επιστρέψει σφάλμα (π.χ. λάθος API key ή πόλη που δεν υπάρχει).
    
    Λειτουργία:
        - Παίρνει το API_KEY από τις περιβαλλοντικές μεταβλητές.
        - Δημιουργεί το url και τα params για το API request.
        - Κάνει αίτημα (GET) στο API.
        - Ελέγχει τον κωδικό απόκρισης και πετάει κατάλληλες εξαιρέσεις αν χρειαστεί.
        - Επιστρέφει τα δεδομένα σε μορφή JSON.
    """
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        # Αν δεν βρεθεί το κλειδί, σταματάμε με σφάλμα
        raise ValueError("Το API key δεν βρέθηκε! Βεβαιώσου ότι υπάρχει στο .env")

    BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,           # Όνομα πόλης προς αναζήτηση
        "appid": API_KEY,    # API key για εξουσιοδότηση
        "units": "metric",   # Μονάδες μέτρησης (Κελσίου)
        "lang": "el"         # Γλώσσα ελληνικά για περιγραφή καιρού
    }

    # Κλήση στο API μέσω HTTP GET
    response = requests.get(BASE_URL, params=params)

    # Έλεγχος του HTTP status code και χειρισμός σφαλμάτων
    if response.status_code == 401:
        raise Exception("❌ Σφάλμα: Invalid API key. Ελέγξτε το API key σας.")
    elif response.status_code == 404:
        raise Exception("❌ Σφάλμα: Η πόλη δεν βρέθηκε.")
    elif response.status_code != 200:
        raise Exception(f"❌ Άγνωστο σφάλμα: {response.status_code}")

    # Επιστρέφουμε το JSON απάντησης του API ως dict
    return response.json()


if __name__ == "__main__":
    """
    Κύριο πρόγραμμα CLI που:
    - Διαβάζει το όνομα της πόλης από τα επιχειρήματα γραμμής εντολών.
    - Καλεί τη συνάρτηση get_weather_data για να πάρει καιρικά δεδομένα.
    - Εκτυπώνει τα στοιχεία καιρού ή εμφανίζει σφάλματα αν υπάρξουν.
    """

    # Έλεγχος ότι ο χρήστης έδωσε το όνομα πόλης ως παράμετρο
    if len(sys.argv) < 2:
        print("Χρήση: python weather.py <πόλη>")
        sys.exit(1)

    city = sys.argv[1]

    try:
        # Λήψη δεδομένων καιρού
        data = get_weather_data(city)

        # Εκτύπωση αποτελεσμάτων με ευανάγνωστο τρόπο
        print(f"🌤 Καιρός στην πόλη {city}: {data['weather'][0]['description']}")
        print(f"🌡 Θερμοκρασία: {data['main']['temp']}°C")
        print(f"💨 Άνεμος: {data['wind']['speed']} m/s")
        print(f"💧 Υγρασία: {data['main']['humidity']}%")
        print(f"🌅 Ανατολή: {datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')}")

    except Exception as e:
        # Εμφάνιση μηνύματος λάθους αν αποτύχει η κλήση στο API
        print(str(e))
