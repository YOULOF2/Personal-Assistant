import praw
from resources import Resources


def return_hot_memes():
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
