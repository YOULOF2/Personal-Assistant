from source.backend.functions.baseClasses import BaseClass
from source.backend.functions.customTypes import SetMethodDict
import requests

_TRIVIA_DB = "https://opentdb.com/api.php"


class GetTrivia(BaseClass):
    def __init__(self):
        super().__init__()
        all_bindings = [
            SetMethodDict(["tell", "trivia"], self.__get_trivia)
        ]
        self._create_binding(all_bindings)

    def __get_trivia(self):
        request_json = requests.get(_TRIVIA_DB, params={"amount": 1}).json()
        joke = request_json.get("results")[0]
        joke_json = {
            "type": joke.get("type"),
            "question": joke.get("question"),
            "correct_answer": joke.get("correct_answer"),
            "incorrect_answers": []
        }
        for incorrect_answer in joke.get("incorrect_answers"):
            joke_json.get("incorrect_answers").append(incorrect_answer)

        return joke_json
