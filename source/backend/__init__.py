import json
from pathlib import Path

# import pafy
import requests
import wikipedia
import yake
from sympy import sympify, solve
from wiktionaryparser import WiktionaryParser
from youtubesearchpython import VideosSearch

from source.backend.todo_list import ToDoList, ToDoItem

class Resources:
    class Endpoints:
        YOUTUBE_SEARCH_RESULTS = "https://www.youtube.com/results"
        YOUTUBE_WATCH = "https://www.youtube.com/watch"

        ANIME_DATABASE_JSON = "https://raw.githubusercontent.com/manami-project/anime-offline-database/master/anime-offline-database-minified.json"


class PersonalAssistant:
    def __init__(self, **kwargs):
        self.__anime_database_path = str(Path(Path(__file__).parent.parent.parent, "assets/anime_database.json"))

    def __init_functions(self):
         # Load Anime Lookup data base of not already loaded
        anime_database_path = str(Path(Path(__file__).parent.parent.parent, "assets/anime_database.json"))

    def __wikipedia_search(self, text):
        return wikipedia.summary(text, sentences=3)

    def __wikitionary_search(self, word):
        parser = WiktionaryParser()
        word = parser.fetch(word)
        definitions = word[0].get("definitions")[0].get("text")
        return definitions

    # @__logger
    # def __youtube_search(self, query):
    #     self.__update_latest_actions()
    #
    #     def video_url(video_id):
    #         video_url = f"{Resources.Endpoints.YOUTUBE_WATCH}?v={video_id}"
    #         video = pafy.new(video_url)
    #         best_quality = video.getbest()
    #         play_url = best_quality.url
    #         return play_url
    #
    #     def audio_url(video_id):
    #         audio_url = f"{Resources.Endpoints.YOUTUBE_WATCH}?v={video_id}"
    #         audio = pafy.new(audio_url)
    #         best_quality = audio.getbestaudio()
    #         play_url = best_quality.url
    #         return play_url
    #
    #     videos_search_results = VideosSearch(query, limit=5).result().get("result")
    #     all_videos_data = []
    #     for video in videos_search_results:
    #         all_videos_data.append(
    #             {
    #                 "best_video": video_url(video.get("id")),
    #                 "best_audio": audio_url(video.get("id")),
    #                 "title": video.get("title"),
    #                 "publishedTime": video.get("publishedTime"),
    #                 "duration": video.get("duration"),
    #                 "viewCount": video.get("viewCount").get("short"),
    #                 "thumbnail": video.get("thumbnails")[0].get("url"),
    #                 "channel": video.get("channel").get("name")
    #             }
    #         )
    #     return all_videos_data

    def __anime_search(self, query):

        if not Path(self.__anime_database_path).is_file():
            database_text = requests.get(Resources.Endpoints.ANIME_DATABASE_JSON).text
            with open(self.__anime_database_path, "w", encoding="utf-8") as file:
                file.write(database_text)

        with open(self.__anime_database_path, encoding="utf-8") as database_file:
            json_data = json.loads(database_file.read())
            all_anime = json_data.get("data")

        all_results = []
        for anime in all_anime:
            anime_title = anime.get("title").lower()
            alternate_titles = [alt_title.lower() for alt_title in anime.get("synonyms")]
            if query.lower() in anime_title or query.lower() in alternate_titles:
                all_results.append(anime)
        return all_results

    def __calculate(self, expression):

        if "=" in expression:
            sympy_eq = sympify("Eq(" + expression.replace("=", ",") + ")")
            return solve(sympy_eq)[0]

        return eval(expression)

    def __extract_keywords(self, text):
        language = "en"
        max_ngram_size = 3
        deduplication_threshold = 0.1
        numOfKeywords = 3
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

