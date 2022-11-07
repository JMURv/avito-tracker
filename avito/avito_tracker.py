from addons.addons import get_session
from bs4 import BeautifulSoup
from time import sleep
import re
from arsenic import get_session, browsers, services

CHROMEDRIVER = 'C:\\Users\\DOROTHY\\PycharmProjects\\avito-tracker\\chrome_driver\\chromedriver.exe'


async def parse_info(page):
    info = {
        'link': '',
        'name': '',
        'img': '',
        'price': '',
        'description': '',
    }
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all("div", {'class': re.compile(r'^iva-item-content')}):
        try:
            info['description'] = link.find('div', {'class': re.compile(r'^iva-item-text')}).text
        except:
            info['description'] = 'Не удалось поучить описание'
        try:
            info['price'] = link.find('meta', {'itemprop': 'price'})['content']
        except:
            info['price'] = 'Не удалось получить цену'
        try:
            info['link'] = f"https://www.avito.ru{link.find('a', {'itemprop': 'url'})['href']}"
        except:
            info['link'] = 'Не удалось получить ссылку'
        try:
            info['name'] = link.find('h3', {'itemprop': 'name'}).text
        except:
            info['name'] = 'Не удалось получить имя'
        try:
            info['img'] = link.findNext('img')['src']
        except:
            info['img'] = 'Не удалось получить картинку'
        break
    return info


async def async_avito(url):
    service = services.Chromedriver(binary=CHROMEDRIVER)
    browser = browsers.Chrome()
    async with get_session(service, browser) as driver:
        await driver.get(url)
        sleep(2)
        html = await driver.get_page_source()
        new_data = await parse_info(html)
        return new_data
