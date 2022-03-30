from resources import Resources
import pafy
from youtubesearchpython import VideosSearch

__all__ = ["return_video_url_youtube", "search_youtube"]


def search_youtube(query):
    videos_search_results = VideosSearch(query, limit=5).result().get("result")
    all_videos_data = []
    for video in videos_search_results:
        all_videos_data.append(
            {
                "id": video.get("id"),
                "title": video.get("title"),
                "publishedTime": video.get("publishedTime"),
                "duration": video.get("duration"),
                "viewCount": video.get("viewCount").get("short"),
                "thumbnail": video.get("thumbnails")[0].get("url"),
                "channel": video.get("channel").get("name")
            }
        )
    return all_videos_data


def return_video_url_youtube(video_id):
    video_url = f"{Resources.Endpoints.YOUTUBE_WATCH}?v={video_id}"
    video = pafy.new(video_url)
    best_quality = video.getbest()
    play_url = best_quality.url
    return play_url
