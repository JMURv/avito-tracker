from bs4 import BeautifulSoup
from time import sleep
import re
from arsenic import get_session, browsers, services
import sys

if sys.platform.startswith('win'):
    CHROMEDRIVER = 'avito_tracker/chrome_driver/chromedriver.exe'
else:
    CHROMEDRIVER = '/root/Projects/avito-tracker/avito_tracker/chrome_driver/chromedriver'


async def parse_info(page):
    avito_url = 'https://www.avito.ru'
    max_words = 500
    info = {
        'link': '',
        'name': '',
        'img': '',
        'price': '',
        'description': '',
    }
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all(
            "div", {'class': re.compile(r'^iva-item-content')}):
        try:
            result = link.find(
                'div', {'class': re.compile(r'^iva-item-text')}).text
            if len(result) > max_words:
                info['description'] = f"{result[:max_words]}..."
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
            info['link'] = f"{avito_url}{result}"
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


async def async_avito(url):
    service = services.Chromedriver(binary=CHROMEDRIVER)
    browser = browsers.Chrome()
    browser.capabilities = {
        "goog:chromeOptions": {
            "args":
                [
                    # "--headless",
                    # "--disable-gpu",
                    # "--no-sandbox",
                    # "--disable-setuid-sandbox",
                    # "--disable-dev-shm-usage",
                    # "--disable-in-process-stack-traces",
                    # "--remote-debugging-port=9222"
                ]
        }
    }
    async with get_session(service, browser) as driver:
        await driver.get(url)
        sleep(2)
        html = await driver.get_page_source()
        new_data = await parse_info(html)
        return new_data
