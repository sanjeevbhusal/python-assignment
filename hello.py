import requests
from requests.exceptions import RequestException
import json
from json.decoder import JSONDecodeError
import sys

ARTICLE_PER_PAGE = 10
ARTICLES_TO_FETCH = 30


def fetch_articles(current_page):
    url = f"https://bg.annapurnapost.com/api/news/list?page={current_page}&per_page={ARTICLE_PER_PAGE}\
    &category_alias=sports"f"&isCategoryPage=1 "
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    except RequestException:
        sys.exit("Oops! Some Error occurred while fetching the Post.")
    else:
        return response.text


def get_existing_articles():
    try:
        with open("news.json", "r") as read_file:
            news = json.load(read_file)
            return news
    except (FileNotFoundError, JSONDecodeError):
        return []


def get_articles():
    total_articles_fetched = 0
    while total_articles_fetched < ARTICLES_TO_FETCH:
        existing_articles = get_existing_articles()
        page_to_fetch = (int(len(existing_articles) / ARTICLE_PER_PAGE)) + 1

        html = fetch_articles(page_to_fetch)
        articles = json.loads(html)["data"]
        updated_articles = articles + existing_articles
        total_articles_fetched += ARTICLE_PER_PAGE

        with open("news.json", "w") as write_file:
            json.dump(updated_articles, write_file, indent=4)

        print(f"Successfully Fetched {len(updated_articles)} articles")


def main():
    print("Fetching News....")
    get_articles()
    print('News have been fetched. Check file called "news.json". ')


if __name__ == "__main__":
    main()
