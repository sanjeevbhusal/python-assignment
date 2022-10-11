import requests
from requests.exceptions import RequestException
import json
import sys

POSTS_PER_PAGE = 21


def fetch_news(current_page):
    if current_page > 1:
        print(f"You already have some news fetched. Program will start fetching from page {current_page}")

    print("Fetching News....")

    url = f"https://bg.annapurnapost.com/api/news/list?page={current_page}&per_page=21&category_alias=sports" \
          f"&isCategoryPage=1 "
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    except RequestException:
        sys.exit("Oops! Some Error occurred while fetching the Post.")
    else:
        return response.text


def get_existing_news():
    with open("news.json", "a+") as f:
        f.seek(0)
        news = f.read()
        return json.loads(news) if len(news) > 0 else []


def get_news():
    existing_news = get_existing_news()
    existing_news_length = len(existing_news)
    page_to_fetch = (int(existing_news_length / POSTS_PER_PAGE)) + 1
    html = fetch_news(page_to_fetch)
    news = json.loads(html)["data"]
    updated_news = news + existing_news
    return json.dumps(updated_news)


def main():
    news_list = get_news()
    with open("news.json", "w") as f:
        f.write(str(news_list))

    print('News have been fetched. Check file called "news.json". ')


if __name__ == "__main__":
    main()
