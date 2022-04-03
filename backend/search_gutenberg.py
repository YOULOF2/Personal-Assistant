import requests
from resources import Resources
from bs4 import BeautifulSoup
from loguru import logger
from pprint import pprint


def search_gutenberg(text):
    parameters = {
        "query": text.replace(" ", "+"),
    }
    request_text = requests.get(Resources.Endpoints.PROJECT_GUTENBERG_SEARCH, params=parameters).text
    soup = BeautifulSoup(request_text, "html.parser")
    all_anchors = soup.find_all("a", class_="link")[3:]
    all_hrefs = [anchor.get("href") for anchor in all_anchors]

    all_titles = [anchor.find(class_="title").text for anchor in all_anchors]
    all_book_ids = [href.removeprefix("/ebooks/") for href in all_hrefs]

    all_books = []
    for title, book_id in zip(all_titles, all_book_ids):
        all_books.append(
            {
                "title": title,
                "book_id": book_id,
            }
        )

    return all_books


def get_book_gutenberg(book_id):
    endpoint = f"{Resources.Endpoints.PROJECT_GUTENBERG_BOOK}{book_id}"
    request_text = requests.get(endpoint).text
    soup = BeautifulSoup(request_text, "html.parser")
    all_tds = soup.find_all("td")
    for td in all_tds:
        anchor_tag = td.find("a", class_="link")
        if anchor_tag is not None:
            if "text/html" in anchor_tag.get("type"):
                book_url = f"{Resources.Endpoints.PROJECT_GUTENBERG_BASE}{anchor_tag.get('href').removeprefix('/')}"
                book_request = requests.get(book_url).text
                soup = BeautifulSoup(book_request, "html.parser")

                book_title = soup.find("h1").text
                chapters_titles = [chapter.find("a") for chapter in soup.find_all("td")]
                chapters_titles = [text.text for text in chapters_titles if text is not None]
                cleaned_chapter_titles = []
                for title in chapters_titles:
                    if not title.isdigit():
                        cleaned_chapter_titles.append(title)
                print("jello")
                all_chapters = []
                for chapter in soup.find_all("div", class_="chapter"):
                    all_p_in_chapter = []
                    for p in chapter.find_all("p"):
                        paragraph_text = p.text.rstrip()
                        all_p_in_chapter.append(paragraph_text)
                    all_chapters.append("\n".join(all_p_in_chapter))

                # print(f"Chapters: {len(cleaned_chapter_titles)}, Text: {len(all_chapters)}")
                book_json = []
                for title, text in zip(cleaned_chapter_titles, all_chapters):
                    book_json.append(
                        {
                            "number": chapters_titles.index(title),
                            "title": title,
                            "content": text,
                        }
                    )
                final_json = {
                    "title": book_title,
                    "content": book_json,
                }
                return final_json
    logger.error("Function executed without returning")


print(get_book_gutenberg(1661))
