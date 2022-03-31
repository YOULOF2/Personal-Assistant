from resources import Resources
import requests

__all__ = ["get_joke"]


def get_joke():
    parameters = {
        "blacklistFlags": "religious,political",
        "type": "single",
        "amount": 1
    }

    request_json = requests.get(Resources.Endpoints.JOKES_API, params=parameters).json()
    joke = request_json.get("joke")
    return joke
