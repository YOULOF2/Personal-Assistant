from source.backend.functions.baseClasses import BaseClass
from source.backend.functions.customTypes import SetMethodDict
import requests

_JOKES_API_ENDPOINT = "https://v2.jokeapi.dev/joke/Any"


class GetJoke(BaseClass):
    def __init__(self):
        super().__init__()
        all_bindings = [
            SetMethodDict(["tell", "joke"], self.__get_joke)
        ]
        self._create_binding(all_bindings)

    def __get_joke(self):
        parameters = {
            "blacklistFlags": "religious,political",
            "type": "single",
            "amount": 1
        }

        request_json = requests.get(_JOKES_API_ENDPOINT, params=parameters).json()
        joke = request_json.get("joke")
        return joke

