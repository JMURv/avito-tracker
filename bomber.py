from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

NUMBER = '9771465424'


def get_session():
    ua = UserAgent()
    options = Options()
    options.add_argument(f'user-agent={ua.chrome}')
    # options.add_argument('--disable-notifications')
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def tele2_handler(driver):
    url = 'https://msk.tele2.ru/login'
    driver.get(url)
    time.sleep(2)
    driver.find_element(By.LINK_TEXT, 'Войти').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//*[@id="keycloakAuth.phone"]').send_keys(NUMBER)
    driver.find_element(By.XPATH, '//*[@id="keycloakLoginModal"]/div/div/div/div/div[2]/form/div[2]/button').click()
    time.sleep(1)


def delivery_handler(driver):
    driver.get('https://www.delivery-club.ru/moscow')
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'header-login-button').click()
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'label--def').send_keys(NUMBER)
    time.sleep(2)


def hh_handler(driver):
    driver.get('https://hh.ru/login')
    time.sleep(2)
    driver.find_element(By.NAME, 'login').send_keys(NUMBER)
    time.sleep(1)
    driver.find_element(By.NAME, 'login').send_keys(Keys.ENTER)
    time.sleep(2)


def all_handler():
    driver = get_session()
    # tele2_handler(driver)
    # delivery_handler(driver)
    hh_handler(driver)


if __name__ == '__main__':
    all_handler()
