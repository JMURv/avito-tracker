from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time


ua = UserAgent()
search = 'rtx%203080'.lower()
url = f'https://www.computeruniverse.net/ru/search?query={search}&sortBy=Prod-ComputerUniverse_ru_price_asc'


def parse_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all("div"):
        if link.attrs.get('class'):
            if link['class'][0].startswith('Headline_default'):
                for new_link in link.find_all('a'):
                    print(new_link.text)


def download_page(url):
    options = Options()
    options.add_argument(f'user-agent={ua.chrome}')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    for i in range(30):
        time.sleep(2)
        html = driver.page_source
        parse_content(html)
        try:
            button = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div[2]/div[2]/ul')
            button[-1].click()
            time.sleep(2)
        except(Exception):
            push = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[1]')
            push.click()
    return


print(download_page(url))
