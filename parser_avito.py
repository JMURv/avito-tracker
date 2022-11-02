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
url = f'https://www.avito.ru/moskva_i_mo/tovary_dlya_kompyutera/komplektuyuschie/videokarty-ASgBAgICAkTGB~pm7gmmZw?cd=1&q=rtx+3080&s=104'


def parse_info(page):
    res = {
        'link': '',
        'name': '',
        'img': '',
        'price': ''
    }
    soup = BeautifulSoup(page, 'html.parser')
    for link in soup.find_all("div", {'class': re.compile(r'^iva-item-content')}):
        a_attr = link.findNext('a')
        img_attr = link.findNext('img')
        res['link'] = a_attr['href']
        res['name'] = a_attr['title']
        res['img'] = img_attr['src']
        for div in link.find_all('div'):
            if div.attrs.get('class'):
                if div['class'][0].startswith('iva-item-priceStep'):
                    meta = div.find('meta', {'itemprop': 'price'})
                    res['price'] = meta['content']
        break
    print(res)


def get_avito(driver):
    driver.get(url)
    time.sleep(2)
    parse_info(driver.page_source)


def get_session():
    ua = UserAgent()
    options = Options()
    options.add_argument(f'user-agent={ua.chrome}')
    # options.add_argument('--disable-notifications')
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def all_handler():
    driver = get_session()
    get_avito(driver)


if __name__ == '__main__':
    all_handler()