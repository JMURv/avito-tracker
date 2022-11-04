import re
import time
from computer_universe.addons import get_session
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from computer_universe.addons import allpage_load

SEARCH_LIST = ['rtx%203080', 'rtx2080']
SEARCH = SEARCH_LIST[-1].lower()
URL = f'https://www.computeruniverse.net/en/search?query={SEARCH}'
PAGES = 50


def parse_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all("li", {'class': re.compile(r'^ais-Hits-item')}):
        name = link.find("a", {'role': 'button'}).text
        href = link.find("a", {'role': 'button'})['href']
        price = link.find("div", {'class': 'price price--grey-alt flex'}).find('span').text
        img = link.find("img", {'alt': name})['src']
        description = []
        for link in link.find_all("li", {'class': 'bullet-points__point'}):
            description.append(link.text)
        description = '\n'.join(description)
        print(name, href, price, img)


def download_page(driver, url):
    driver.get(url)
    for page in range(1, PAGES+1):
        time.sleep(3)
        try:
            allpage_load(driver)
            html = driver.page_source
            parse_content(html)
        except(Exception):
            continue
        finally:
            pre = driver.find_elements(By.CLASS_NAME, 'Pagination__naviButton.false')[-1]
            pre.find_element(By.CLASS_NAME, 'Pagination__naviButton__inner').click()
    return


if __name__ == '__main__':
    driver = get_session()
    download_page(driver, URL)
