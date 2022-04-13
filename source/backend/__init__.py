import functools
import inspect
from os import getenv
from random import choice

import pafy
import praw
import requests
import wikipedia
import yake
from dotenv import load_dotenv
from loguru import logger
from sympy import sympify, solve
from wiktionaryparser import WiktionaryParser
from youtubesearchpython import VideosSearch

from source.backend.todo_list import ToDoList, ToDoItem

load_dotenv()


class Resources:
    class Secrets:
        LONGITUDE = getenv("LONGITUDE")
        LATITUDE = getenv("LATITUDE")
        OPENWEATHERMAP_API_KEY = getenv("OPEN_WEATHER_MAP_API_KEY")
        REDDIT_PRAW_API_KEY = getenv("REDDIT_PRAW_API_KEY")
        REDDIT_PRAW_API_USER_KEY = getenv("REDDIT_PRAW_API_USER_KEY")

    class Endpoints:
        OPEN_WEATHER_API = "https://api.openweathermap.org/data/2.5/weather"
        YOUTUBE_SEARCH_RESULTS = "https://www.youtube.com/results"
        YOUTUBE_WATCH = "https://www.youtube.com/watch"
        JOKES_API = "https://v2.jokeapi.dev/joke/Any"
        TRIVIA_DB = "https://opentdb.com/api.php"

    class Constants:
        POSSIBLE_FAVOURITES_LIST = [
            "Chicken Burger",
            "Chicken Cheese Burger",

            "Beef Burger",
            "Beef Cheese Burger",

            "Cheese Pizza",
            "Pepperoni Pizza",
            "Chicken Pizza",
            "SeaFood Pizza"
        ]


class PersonalAssistant:
    def __init__(self, **kwargs):
        self.assistant_name = kwargs.get("PersonalName")
        self.assistant_favourites = [choice(Resources.Constants.POSSIBLE_FAVOURITES_LIST) for _ in range(3)]
        self.mood = 50

        self.user_name = kwargs.get("Username")
        self.user_favourites = kwargs.get("UserFavourites")

        self.__last_actions = []

    @staticmethod
    def __logger(function):
        @functools.wraps(function)
        def wrapper(*args, **kwargs):
            logger.debug(f"'{function.__name__}' function has been called", colors=True)
            return function(*args, **kwargs)
        return wrapper

    def __update_latest_actions(self):
        function_name = str(inspect.stack()[1].function).removeprefix("__")

        self.__last_actions.append(function_name)

    @__logger
    def __get_joke(self):
        self.__update_latest_actions()

        parameters = {
            "blacklistFlags": "religious,political",
            "type": "single",
            "amount": 1
        }

        request_json = requests.get(Resources.Endpoints.JOKES_API, params=parameters).json()
        joke = request_json.get("joke")
        return joke

    @__logger
    def __get_hot_memes(self):
        self.__update_latest_actions()

        reddit_client = praw.Reddit(
            client_id=Resources.Secrets.REDDIT_PRAW_API_USER_KEY,
            client_secret=Resources.Secrets.REDDIT_PRAW_API_KEY,
            user_agent="Personal-Assistant",
        )

        subreddit = reddit_client.subreddit("memes")

        hot_memes = []
        for post in subreddit.hot(limit=20):
            post_title = post.title
            post_url = str(post.url)

            if "https://v.redd.it/" in post_url:
                pass
            else:
                hot_memes.append(
                    {
                        "title": post_title,
                        "url": post_url,
                        "rating": post.score
                    }
                )

        return hot_memes

    @__logger
    def __get_trivia(self):
        self.__update_latest_actions()

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

    @__logger
    def __get_weather(self):
        self.__update_latest_actions()

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

    @__logger
    def __wikipedia_search(self, text):
        self.__update_latest_actions()

        return wikipedia.summary(text, sentences=3)

    @__logger
    def __dictionary_search(self, word):
        self.__update_latest_actions()

        parser = WiktionaryParser()
        word = parser.fetch(word)
        definitions = word[0].get("definitions")[0].get("text")
        return definitions

    @__logger
    def __youtube_search(self, query):
        self.__update_latest_actions()

        def video_url(video_id):
            video_url = f"{Resources.Endpoints.YOUTUBE_WATCH}?v={video_id}"
            video = pafy.new(video_url)
            best_quality = video.getbest()
            play_url = best_quality.url
            return play_url

        def audio_url(video_id):
            audio_url = f"{Resources.Endpoints.YOUTUBE_WATCH}?v={video_id}"
            audio = pafy.new(audio_url)
            best_quality = audio.getbestaudio()
            play_url = best_quality.url
            return play_url

        videos_search_results = VideosSearch(query, limit=5).result().get("result")
        all_videos_data = []
        for video in videos_search_results:
            all_videos_data.append(
                {
                    "best_video": video_url(video.get("id")),
                    "best_audio": audio_url(video.get("id")),
                    "title": video.get("title"),
                    "publishedTime": video.get("publishedTime"),
                    "duration": video.get("duration"),
                    "viewCount": video.get("viewCount").get("short"),
                    "thumbnail": video.get("thumbnails")[0].get("url"),
                    "channel": video.get("channel").get("name")
                }
            )
        return all_videos_data

    @__logger
    def __calculate(self, expression):
        self.__update_latest_actions()

        if "=" in expression:
            sympy_eq = sympify("Eq(" + expression.replace("=", ",") + ")")
            return solve(sympy_eq)[0]

        return eval(expression)

    @__logger
    def __extract_keywords(self, text):
        language = "en"
        max_ngram_size = 3
        deduplication_threshold = 0.1
        numOfKeywords = 5
        kw_extractor = yake.KeywordExtractor(lan=language, n=max_ngram_size, dedupLim=deduplication_threshold,
                                             top=numOfKeywords)
        keywords = kw_extractor.extract_keywords(text)

        refined_keywords = [keyword[0] for keyword in keywords]

        text_list = []
        for extracted_text in refined_keywords:
            for segment in extracted_text.split(" "):
                text_list.append(segment)
        text_list = list(set(text_list))

        if "my" in text:
            text_list.append("my")
        elif "your" in text:
            text_list.append("your")

        return text_list

    @__logger
    def process(self, text):
        keywords_list = self.__extract_keywords(text)
        print(keywords_list)

    @__logger
    def test_function(self):
        print(self.__youtube_search("jacksepticeye"))
        self.__update_latest_actions()
        print(self.__last_actions)


