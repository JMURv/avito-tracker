from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import re

ua = UserAgent()
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


def get_session():
    ua = UserAgent()
    options = Options()
    options.add_argument(f'user-agent={ua.chrome}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def all_handler(driver):
    get_avito(driver)


if __name__ == '__main__':
    driver = get_session()
    all_handler(driver)
    driver.quit()
