import requests
from resources import Resources

__all__ = ["get_trivia"]


def get_trivia():
    request_json = requests.get(Resources.Endpoints.TRIVIA_DB, params={"amount": 1}).json()
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
