import requests
from requests.exceptions import RequestException
import json
from json.decoder import JSONDecodeError
import sys


ARTICLES_TO_FETCH = 30


def fetch_articles(current_page):
    article_per_page = 10
    url = f"https://bg.annapurnapost.com/api/news/list?page={current_page}&per_page={article_per_page}\
    &category_alias=sports"f"&isCategoryPage=1 "
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    except RequestException:
        sys.exit("Oops! Some Error occurred while fetching the Post.")
    else:
        return response.json()


def get_existing_articles_detail():
    try:
        with open("news.json", "r") as read_file:
            json_data = json.load(read_file)
            return json_data.get("articles"), json_data.get("last_fetched_page")
    except (FileNotFoundError, JSONDecodeError):
        return [], 0


def get_articles():
    current_articles_fetched = 0
    existing_articles, last_fetched_page = get_existing_articles_detail()

    while current_articles_fetched < ARTICLES_TO_FETCH:
        page_to_fetch = last_fetched_page + 1
        articles = fetch_articles(page_to_fetch).get("data")
        # we don't have any more articles on this subject
        if len(articles) == 0:
            break
        existing_articles += articles
        current_articles_fetched += len(articles)

        with open("news.json", "w") as write_file:
            json.dump({"last_fetched_page": page_to_fetch, "articles": existing_articles}, write_file, indent=4)

        print(f"Successfully Fetched {len(existing_articles)} articles")


def main():
    print("Fetching News....")
    get_articles()
    print('News have been fetched. Check file called "news.json". ')


if __name__ == "__main__":
    main()
