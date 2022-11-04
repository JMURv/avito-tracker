from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from computer_universe.addons import allpage_load
import time
import re

ua = UserAgent()
search = 'PlayStation+5'
PAGES = 15
url = f'https://www.amazon.com/s?k={search}'
# url = 'https://www.amazon.com/s?k={PlayStation+5}&page={2}'


def parse_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all("div", {'class': re.compile(r'^s-result-item')}):
        name = link.find('span', {'class': 'a-size-medium a-color-base a-text-normal'})
        print(name)


def amazon_parse(driver):
    driver.get(url)
    for page in range(1, PAGES+1):
        time.sleep(2)
        allpage_load(driver)
        html = driver.page_source
        parse_content(html)
        try:
            driver.find_element(By.LINK_TEXT, 'Next').click()
            time.sleep(2)
            continue
        except(Exception):
            break
    return


def get_session():
    ua = UserAgent()
    options = Options()
    options.add_argument(f'user-agent={ua.chrome}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


if __name__ == '__main__':
    driver = get_session()
    amazon_parse(driver)
    driver.quit()
