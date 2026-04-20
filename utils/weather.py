"""Weather API wrapper for Ladakh locations."""

import os
import requests


# Mapping of common names to coordinates
LADAKH_LOCATIONS = {
    "leh": {"lat": 34.1526, "lon": 77.5771, "name": "Leh"},
    "nubra": {"lat": 34.5500, "lon": 77.6500, "name": "Nubra Valley"},
    "nubra valley": {"lat": 34.5500, "lon": 77.6500, "name": "Nubra Valley"},
    "diskit": {"lat": 34.5400, "lon": 77.5600, "name": "Diskit"},
    "hunder": {"lat": 34.5800, "lon": 77.6300, "name": "Hunder"},
    "pangong": {"lat": 33.7500, "lon": 78.6500, "name": "Pangong Lake"},
    "pangong lake": {"lat": 33.7500, "lon": 78.6500, "name": "Pangong Lake"},
    "pangong tso": {"lat": 33.7500, "lon": 78.6500, "name": "Pangong Lake"},
    "tso moriri": {"lat": 32.9700, "lon": 78.2800, "name": "Tso Moriri"},
    "kargil": {"lat": 34.5539, "lon": 76.1347, "name": "Kargil"},
    "zanskar": {"lat": 33.5000, "lon": 76.9000, "name": "Zanskar"},
    "lamayuru": {"lat": 34.2800, "lon": 76.7800, "name": "Lamayuru"},
    "alchi": {"lat": 34.2300, "lon": 76.8500, "name": "Alchi"},
    "thiksey": {"lat": 34.0500, "lon": 77.5800, "name": "Thiksey"},
    "hemis": {"lat": 33.9800, "lon": 77.6200, "name": "Hemis"},
}


def get_weather_for_location(location: str) -> str:
    """Fetch weather for a Ladakh location using Open-Meteo (free, no API key needed)."""
    
    # Find matching location
    loc_key = location.lower().strip()
    coords = None
    
    for key, val in LADAKH_LOCATIONS.items():
        if key in loc_key or loc_key in key:
            coords = val
            break
    
    if not coords:
        # Default to Leh
        coords = LADAKH_LOCATIONS["leh"]
    
    try:
        # Open-Meteo free API — no key required
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m,weather_code",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code",
            "timezone": "Asia/Kolkata",
            "forecast_days": 3,
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        current = data["current"]
        daily = data["daily"]
        
        weather_codes = {
            0: "Clear sky ☀️", 1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅",
            3: "Overcast ☁️", 45: "Fog 🌫️", 48: "Rime fog 🌫️",
            51: "Light drizzle 🌦️", 53: "Drizzle 🌦️", 55: "Heavy drizzle 🌧️",
            61: "Light rain 🌦️", 63: "Rain 🌧️", 65: "Heavy rain 🌧️",
            71: "Light snow 🌨️", 73: "Snow 🌨️", 75: "Heavy snow ❄️",
            80: "Light showers 🌦️", 81: "Showers 🌧️", 82: "Heavy showers ⛈️",
            95: "Thunderstorm ⛈️", 96: "Thunderstorm with hail ⛈️",
        }
        
        current_weather = weather_codes.get(current["weather_code"], "Unknown")
        
        result = f"**Weather for {coords['name']} (Ladakh):**\n\n"
        result += f"**Now:**\n"
        result += f"- Condition: {current_weather}\n"
        result += f"- Temperature: {current['temperature_2m']}°C\n"
        result += f"- Humidity: {current['relative_humidity_2m']}%\n"
        result += f"- Wind: {current['wind_speed_10m']} km/h\n\n"
        
        result += f"**3-Day Forecast:**\n"
        for i in range(len(daily["time"])):
            day_weather = weather_codes.get(daily["weather_code"][i], "Unknown")
            result += (
                f"- {daily['time'][i]}: {day_weather}, "
                f"{daily['temperature_2m_min'][i]}°C to {daily['temperature_2m_max'][i]}°C, "
                f"Rain: {daily['precipitation_sum'][i]}mm\n"
            )
        
        result += (
            f"\n⚠️ **Altitude note:** {coords['name']} is at high altitude. "
            f"Temperatures can drop sharply after sunset. Carry warm layers even in summer."
        )
        
        return result
        
    except requests.RequestException as e:
        return (
            f"Unable to fetch live weather data for {coords['name']} right now. "
            f"General guidance: Leh averages 5-25°C in summer (Jun-Sep) and -20 to -5°C in winter. "
            f"Always check weather before mountain passes — conditions change rapidly."
        )
