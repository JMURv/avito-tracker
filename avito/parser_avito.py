from computer_universe.addons import get_session
from bs4 import BeautifulSoup
import time
import re


url = 'https://www.avito.ru/moskva_i_mo/tovary_dlya_kompyutera/komplektuyuschie/videokarty-ASgBAgICAkTGB~pm7gmmZw?cd=1&q=rtx+3080&s=104'
PREVIOUS_DATA = {}


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
            info['link'] = link.find('a', {'itemprop': 'url'})['href']
            info['name'] = link.find('h3', {'itemprop': 'name'}).text
            info['img'] = link.findNext('img')['src']
            break
        except(Exception):
            continue
    return info


def get_avito(driver, prev=PREVIOUS_DATA):
    driver.get(url)
    time.sleep(2)
    new_data = parse_info(driver.page_source)
    if new_data != prev:
        prev = new_data  # Sent new info
    return prev


if __name__ == '__main__':
    driver = get_session()
    get_avito(driver)
    driver.quit()