import argparse
import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

ENDPOINT = "https://api-ssl.bitly.com/v4"


def shorten_link(url_to_shorten, headers):
    payload = {
        "long_url": url_to_shorten
    }
    response = requests.post(
        f"{ENDPOINT}/shorten", 
        json=payload, 
        headers=headers
        )
    response.raise_for_status() 
    return f"Битлинк: {response.json()['link']}"


def count_clicks(bitlink, headers):
    payload = {
        "units": -1,
    }
    response = requests.get(
        f"{ENDPOINT}/bitlinks/{bitlink}/clicks/summary", 
        headers=headers, 
        params=payload
        )
    response.raise_for_status() 
    return f"Общее количество переходов: {response.json()['total_clicks']}"


def get_clear_url(url):
    parsed_link = urlparse(url)
    if parsed_link.hostname:
        return parsed_link.hostname + parsed_link.path
    else:
        return url


def is_bitlink(url, headers):
    response = requests.get(
        f"{ENDPOINT}/bitlinks/{url}",
        headers=headers
        )
    return response.ok


def main():
    parser = argparse.ArgumentParser(
        description="Укорачивает ссылку или возвращает количество переходов по короткой ссылке"
    )
    parser.add_argument('url', help='Введите ссылку')
    args = parser.parse_args()
    user_url = args.url

    load_dotenv()

    API_TOKEN = os.environ["BITLY_API_TOKEN"]

    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        clear_url = get_clear_url(user_url)
        if is_bitlink(clear_url, headers):
            print(count_clicks(clear_url, headers))
        else:
            print(shorten_link(user_url, headers))
    except requests.exceptions.HTTPError:
        print("Неправильно введена ссылка")



if __name__ == "__main__":
    main()
