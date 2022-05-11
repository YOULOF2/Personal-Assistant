from source.backend.functions.baseClasses import BaseClass
from source.backend.functions.customTypes import SetMethodDict
import praw
from dotenv import load_dotenv
from os import getenv

load_dotenv()

_REDDIT_PRAW_API_KEY = getenv("REDDIT_PRAW_API_KEY")
_REDDIT_PRAW_API_USER_KEY = getenv("REDDIT_PRAW_API_USER_KEY")


class GetHottestMemes(BaseClass):
    def __init__(self):
        super().__init__()

        all_bindings = [
            SetMethodDict(["get", "memes"], self.__get_hot_memes)
        ]
        self._create_binding(all_bindings)

    def __get_hot_memes(self):
        reddit_client = praw.Reddit(
            client_id=_REDDIT_PRAW_API_KEY,
            client_secret=_REDDIT_PRAW_API_USER_KEY,
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
