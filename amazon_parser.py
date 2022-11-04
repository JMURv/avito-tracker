from addons.addons import allpage_load, get_session
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re

search = 'PlayStation+5'
PAGES = 15
url = f'https://www.amazon.com/s?k={search}'


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
        parse_content(driver.page_source)
        try:
            driver.find_element(By.LINK_TEXT, 'Next').click()
            time.sleep(2)
            continue
        except(Exception):
            break
    return


if __name__ == '__main__':
    driver = get_session()
    amazon_parse(driver)
    driver.quit()
