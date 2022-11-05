from addons.addons import get_session
from bs4 import BeautifulSoup
import time
import re

# url = 'https://www.avito.ru/moskva_i_mo/tovary_dlya_kompyutera/komplektuyuschie/videokarty-ASgBAgICAkTGB~pm7gmmZw?cd=1&q=rtx+3080&s=104'
PREV = {}


def parse_info(page):
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
        except(Exception):
            continue
    return info


def get_avito(url):
    driver = get_session()
    driver.get(url)
    time.sleep(2)
    new_data = parse_info(driver.page_source)
    driver.quit()
    return new_data
