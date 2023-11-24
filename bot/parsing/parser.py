import requests
from bs4 import BeautifulSoup
import re


BASE_URL = 'https://www.avito.ru'
MAX_DESCRIPTION_WORDS_LENGTH = 40


def parse_info(page: str) -> dict[str, str]:
    info = {
        'link': '',
        'name': '',
        'img': '',
        'price': '',
        'description': '',
    }
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all(
            "div", {'class': re.compile(r'^iva-item-content')}, limit=1):
        try:
            result = link.find('div', {
                'class': re.compile(r'^iva-item-description')
            }).text
            if len(result.split(' ')) > MAX_DESCRIPTION_WORDS_LENGTH:
                new = ' '.join(
                    result.split(' ')[:MAX_DESCRIPTION_WORDS_LENGTH]
                )
                info['description'] = f"{new}..."
            else:
                info['description'] = result
        except Exception:
            info['description'] = 'Не удалось поучить описание'

        try:
            info['price'] = link.find(
                'meta', {'itemprop': 'price'})['content']
        except Exception:
            info['price'] = 'Не удалось получить цену'

        try:
            result = link.find(
                'a', {'itemprop': 'url'})['href']
            info['link'] = f"{BASE_URL}{result}"
        except Exception:
            info['link'] = 'Не удалось получить ссылку'

        try:
            info['name'] = link.find(
                'h3', {'itemprop': 'name'}).text
        except Exception:
            info['name'] = 'Не удалось получить имя'

        try:
            info['img'] = link.findNext('img')['src']
        except Exception:
            info['img'] = 'Не удалось получить картинку'

        break
    return info


def sync_avito(url: str):
    print(f'start parsing for {url}')
    response = requests.get(url)
    response.raise_for_status()
    new_data = parse_info(response.text)
    return new_data
