import pytest
from unittest.mock import patch
import weather
import os

def test_api_key_missing(monkeypatch):
    """Το API key πρέπει να υπάρχει αλλιώς σηκώνει ValueError"""
    monkeypatch.delenv("API_KEY", raising=False)
    with pytest.raises(ValueError):
        weather.get_weather_data("Athens")

@patch("weather.requests.get")
def test_successful_response(mock_get):
    """Έλεγχος αν γίνεται σωστά η ανάγνωση από το API"""
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {
        "weather": [{"description": "αίθριος"}],
        "main": {"temp": 25},
        "wind": {"speed": 3}
    }

    result = weather.get_weather_data("Athens")
    assert result["main"]["temp"] == 25
    assert result["weather"][0]["description"] == "αίθριος"

@patch("weather.requests.get")
def test_city_not_found(mock_get):
    """Το API επιστρέφει 404 αν η πόλη δεν βρεθεί"""
    mock_get.return_value.status_code = 404

    with pytest.raises(Exception) as excinfo:
        weather.get_weather_data("UnknownCity")
    assert "Η πόλη δεν βρέθηκε" in str(excinfo.value)
