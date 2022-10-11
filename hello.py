import requests
from requests.exceptions import RequestException
import json
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
        print(f"Successfully Fetched {current_page * 10} articles")
        return response.text


def get_existing_articles():
    with open("news.json", "a+") as f:
        f.seek(0)
        news = f.read()
        return json.loads(news) if len(news) > 0 else []


def get_articles():
    total_articles_fetched = 0
    while total_articles_fetched < ARTICLES_TO_FETCH:
        existing_articles = get_existing_articles()
        page_to_fetch = (int(len(existing_articles) / ARTICLE_PER_PAGE)) + 1

        html = fetch_articles(page_to_fetch)
        articles = json.loads(html)["data"]
        updated_articles = articles + existing_articles
        total_articles_fetched += ARTICLE_PER_PAGE

        with open("news.json", "w") as f:
            f.write(str(json.dumps(updated_articles)))


def main():
    print("Fetching News....")
    get_articles()
    print('News have been fetched. Check file called "news.json". ')


if __name__ == "__main__":
    main()
