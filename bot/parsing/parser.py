from time import sleep
from loguru import logger
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


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
            info['img'] = None

        break
    return info


def sync_avito(url: str):
    logger.debug(f"Start parsing for: {url}")
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
        sleep(5)
        page_source = driver.page_source
        logger.success(driver.title)
        driver.close()
        driver.quit()
        return parse_info(page_source)
    except Exception as ex:
        logger.error(f"Selenium error: {ex}")
        driver.close()
        driver.quit()
        return None
