from pathlib import Path
from dotenv import load_dotenv
from os import getenv

__all__ = ["Resources"]

load_dotenv()


def path_to_file(path):
    return str(Path(Path(__file__).resolve().parent, path).resolve())


class Resources:

    class Secrets:
        LONGITUDE = getenv("LONGITUDE")
        LATITUDE = getenv("LATITUDE")
        OPENWEATHERMAP_API_KEY = getenv("OPEN_WEATHER_MAP_API_KEY")

    class Endpoints:
        OPEN_WEATHER_API = "https://api.openweathermap.org/data/2.5/weather"
        YOUTUBE_SEARCH_RESULTS = "https://www.youtube.com/results"
        YOUTUBE_WATCH = "https://www.youtube.com/watch"
        JOKES_API = "https://v2.jokeapi.dev/joke/Any"
        TRIVIA_DB = "https://opentdb.com/api.php"

