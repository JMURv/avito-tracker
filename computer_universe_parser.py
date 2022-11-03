import re
import time
from computer_universe.addons import get_session
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from computer_universe.addons import page_wait, get_right_xpath


SEARCH = 'rtx%203080'.lower()
URL = f'https://www.computeruniverse.net/en/search?query={SEARCH}'
PAGES = 50
DIGIT = 7


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
        print(name)


def download_page(driver, url):
    driver.get(url)
    for page in range(1, PAGES+1):
        time.sleep(3)
        page_wait(driver)
        html = driver.page_source
        parse_content(html)
        try:
            driver.find_element(
                By.XPATH, f'//*[@id="main-content"]/div[2]/div[2]/ul/li[{get_right_xpath(page, DIGIT)}]/button'
            ).click()
            continue
        except(Exception):
            continue
    return


if __name__ == '__main__':
    driver = get_session()
    download_page(driver, URL)
