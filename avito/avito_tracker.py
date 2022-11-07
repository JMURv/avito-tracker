from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from addons.addons import get_session
from bs4 import BeautifulSoup
from time import sleep
import re
import asyncio
from arsenic import get_session, browsers, services

CHROMEDRIVER = 'C:\\Users\\Archi\\PycharmProjects\\avito-tracker\\chrome_driver\\chromedriver.exe'


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
            info['price'] = link.find('meta', {'itemprop': 'price'})['content']
            info['link'] = f"https://www.avito.ru{link.find('a', {'itemprop': 'url'})['href']}"
            info['name'] = link.find('h3', {'itemprop': 'name'}).text
            info['img'] = link.findNext('img')['src']
            break
        except Exception:
            continue
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


# def get_avito(url):
#     driver = get_session()
#     driver.get(url)
#     time.sleep(2)
#     new_data = parse_info(driver.page_source)
#     driver.quit()
#     return new_data
#
#
# def multi(pages):
#     result = []
#     with ThreadPoolExecutor() as executor:
#         for page in executor.map(get_avito, pages):
#             result.append(page)
#         return result
