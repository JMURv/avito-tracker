from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


ua = UserAgent()
search = 'rtx%203080'.lower()
url = f'https://www.computeruniverse.net/en/search?query={search}'

PAGES = 15


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
    options.add_argument('--disable-notifications')
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    for page in range(1, PAGES):
        driver.get(url)
        time.sleep(2)
        html = driver.page_source
        parse_content(html)
        try:
            button = driver.find_elements(By.XPATH, '//*[@id="main-content"]/div[2]/div[2]/ul')[-1]
            button.click()
            url = driver.current_url
            continue
        except(Exception):
            print('End')
    return


if __name__ == '__main__':
    print(download_page(url))
