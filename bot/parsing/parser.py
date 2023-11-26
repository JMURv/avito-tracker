from loguru import logger
import requests
from bs4 import BeautifulSoup
import re


BASE_URL = 'https://www.avito.ru'
MAX_DESCRIPTION_WORDS_LENGTH = 40
COOKIES_DICT = {
    "buyer_from_page": "catalog",
    "tmr_detect": "0%7C1701037570317",
    "abp": "0",
    "sx": "H4sIAAAAAAAC%2FwTAUQ7CIAwG4Lv8zz603Wg3brNBFY2ZxsQJIdzdr4PUg4ZMk1nWJHlPbL7slq5CvhAhdpyIkPb%2B%2BaPO5c4br%2FU4Cn9ovpXnaa9v23CBI7IRs0yrhjH%2BAQAA%2F%2F90rl7hWwAAAA%3D%3D",
    "_ga_WW6Q1STJ8M": "GS1.1.1701037607.2.0.1701037767.0.0.0",
    "dfp_group": "71",
    "ft": "aiK0vHNk2R3SqngNHRQBf+LiPzNqqAvWs7neL8wcpvUYxEWVhVyJ1zXXTpbHYZrO+nw7SxXdAhOD9fpcnsDKLi8MZv9ikdZ7Y2GHIMnKgB03oSIIfZMhhtbF2p1c+xBfLLMsFLto3emCbuc8QPuq2tEeuanyO4XxxIWJfI0WyanBPK/vNwdC+Tk+89pAAkb5",
    "_ym_isad": "1",
    "_gcl_au": "1.1.2060561681.1700748855",
    "tmr_lvid": "b964e4236798f933e5b0dbe30e784356",
    "fgsscw-avito": "7v1c70f7a234c14286d07774a4c2963392b48378",
    "advcake_session_id": "b3d0d893-deca-b6ba-4748-ca384abd8cca",
    "gsscw-avito": "/gwtsu8XtrRsVhcbj88zsLxmSigXyGXBSN+Fh2CpjZsnrJnq9HO1KRbSEKvjVc62KW4J4yP7Qk9+9DGNvO7E13931WUDZF+tU+B5db6r6kY0DMiDvpiG4Yyu+Bg53dcWtxWzPcxJ42+iCQSE8j15g5PWic/6JZZ3T+nw6ZFmEe+/nfHD39yYY9T5POnADW0m7nM9rAgRU3A1rxhIXQEKf7abRt803O6dQFOnq8PQA24xdPQuBu4u3slolgjksA==",
    "gMltIuegZN2COuSe": "EOFGWsm50bhh17prLqaIgdir1V0kgrvN",
    "cfidsw-avito": "icL7bZ9YBXlpyOECbfRAfi8lSaOvpNLANLIIhgCHz5s4/KDAJ6WaY7M5SKjc3yex4bwZU0nJAvjfoihKZjZ5sr6HJLm23QIYr2b4UIVYUPLXpC6PUainfMNbblzca2OsI87hJAoim0pYRMN6f1QBVvxzOivvI/COlGGFSw==",
    "srv_id": "gqepgUBd78CPKwaZ.yfjmuvS2JSO61Umfi7t3YUXcxOMkQ-HuduDZgsVyocM-qbP_KAS8hMpqGtV_lOQSG0Da.rR0TB96wJeK_fVVjP-kiPQvswNC18kTJoIZmK7oKCJc=.web",
    "v": "1701037560",
    "_ym_d": "1700748855",
    "yandex_monthly_cookie": "true",
    "u": "2y6cr19e.oxorza.18abjpwso9s00",
    "_ym_visorc": "b",
    "_ym_uid": "1700748855728297799",
    "_ga": "GA1.1.853262274.1700748855",
    "__zzatw-avito": "MDA0dBA=Fz2+aQ==",
    "cfidsw-avito": "T9SbnQB1Jp5ZoewQfdBWNk6rc93ZPswY9ckfz3l2dQk+rfKYKZjUttQP4Nw+15jMl0wexQySpGkUa5iGVKVKk5bhUeQ/fgzY6Co76GU8Jc3UEtXdrn6/pdjBPqkdvCZ9My0Mm3oua8XG19ZN1mhZ0VNeAcIlVvpixG2vyg==",
    "tmr_lvidTS": "1700748834389",
    "f": "5.9fd3735f16182a2836b4dd61b04726f147e1eada7172e06c47e1eada7172e06c47e1eada7172e06c47e1eada7172e06cb59320d6eb6303c1b59320d6eb6303c1b59320d6eb6303c147e1eada7172e06c8a38e2c5b3e08b898a38e2c5b3e08b890df103df0c26013a0df103df0c26013a2ebf3cb6fd35a0ac0df103df0c26013a8b1472fe2f9ba6b9ad42d01242e34c7968e2978c700f15b6bf11f980bc2bc377f2c082410b22639b04dbcad294c152cb0df103df0c26013aba0ac8037e2b74f971e7cb57bbcb8e0f03c77801b122405c8b1472fe2f9ba6b91d6703cbe432bc2a71e7cb57bbcb8e0f03c77801b122405c2da10fb74cac1eab2da10fb74cac1eab2ebf3cb6fd35a0ac20f3d16ad0b1c546b892c6c84ad16848a9b4102d42ade879dcb5a55b9498f642b81f1c77c4dcf4df4fb29506e8757e3ca9afb448c9611b8cf2a3e19032a3d2d34525907271a6a0ebc40e010b6d3726f9c9d45c56e090700391e52da22a560f550df103df0c26013a0df103df0c26013aaaa2b79c1ae9259553283d121b8f9a9b838f794c4e5a47a63de19da9ed218fe2c772035eab81f5e123f5e56da7ec04f4a1a4201a28a6ec9b059080ed9becc4cd",
    "uxs_uid": "952dd920-8a0a-11ee-9b14-5f55d8fae188",
    "advcake_track_id": "1d691ab9-1000-a8ea-1fea-37a80c1035ca"
}


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
            error_message = "Не удалось получить описание"
            logger.debug(error_message)
            info['description'] = error_message

        try:
            info['price'] = link.find(
                'meta', {'itemprop': 'price'})['content']
        except Exception:
            error_message = "Не удалось получить цену"
            logger.debug(error_message)
            info['price'] = error_message

        try:
            result = link.find(
                'a', {'itemprop': 'url'})['href']
            info['link'] = f"{BASE_URL}{result}"
        except Exception:
            error_message = "Не удалось получить ссылку"
            logger.debug(error_message)
            info['link'] = error_message

        try:
            info['name'] = link.find(
                'h3', {'itemprop': 'name'}).text
        except Exception:
            error_message = "Не удалось получить имя"
            logger.debug(error_message)
            info['name'] = error_message

        try:
            info['img'] = link.findNext('img')['src']
        except Exception:
            error_message = "Не удалось получить картинку"
            logger.debug(error_message)
            info['img'] = error_message

        break
    return info


def sync_avito(url: str):
    logger.debug(f"Start parsing for: {url}")
    response = requests.get(
        url=url,
        cookies=COOKIES_DICT
    )
    if response.status_code == 200:
        logger.debug(f"Successful parse")
        return parse_info(response.text)
    else:
        logger.debug(
            f"Error while parsing. Status code: {response.status_code}"
        )
        return None
