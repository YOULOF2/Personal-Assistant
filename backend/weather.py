from resources import Resources
import requests

__all__ = ["get_weather"]


def get_weather():
    ENDPOINT = Resources.Endpoints.OPEN_WEATHER_API

    PARAMETERS = {
        "appid": Resources.Secrets.OPENWEATHERMAP_API_KEY,
        "lat": Resources.Secrets.LATITUDE,
        "lon": Resources.Secrets.LONGITUDE,
        "units": "metric",
    }

    request = requests.get(ENDPOINT, params=PARAMETERS)
    weather_json = request.json()
    final_json = {
        "Main": weather_json.get("weather")[0].get("main"),
        "Description": weather_json.get("weather")[0].get("description"),
        "temp": weather_json.get("main").get("temp"),
        "feels_like": weather_json.get("main").get("feels_like"),
        "humidity": f'{weather_json.get("main").get("feels_like")} percent'
    }
    return final_json
