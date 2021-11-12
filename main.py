import argparse
import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse

parser = argparse.ArgumentParser(
    description="Укорачивает ссылку или возвращает количество переходов по короткой ссылке"
)
parser.add_argument('url', help='Введите ссылку')
args = parser.parse_args()

load_dotenv()

API_TOKEN = os.environ["BITLY_API_TOKEN"]
ENDPOINT = "https://api-ssl.bitly.com/v4"

headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Content-Type": "application/json"
    }


def shorten_link(url_to_shorten):
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


def count_clicks(bitlink):
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


def is_bitlink(url):
    response = requests.get(
        f"{ENDPOINT}/bitlinks/{url}",
        headers=headers
        )
    return response.ok


def main(url):
    try:
        clear_url = get_clear_url(url)
        if is_bitlink(clear_url):
            return count_clicks(clear_url)
        else:
            return shorten_link(url)
    except requests.exceptions.HTTPError:
        return "Неправильно введена ссылка"



if __name__ == "__main__":
    # print(main(input("Введите ссылку: ")))
    print(main(args.url))
