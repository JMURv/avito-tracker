from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from addons.addons import get_session
import time


NUMBER = '9771465424'


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


def mvideo_handler(driver):
    driver.get('https://www.mvideo.ru/login')
    time.sleep(2)
    driver.find_element(By.CLASS_NAME, 'old_br_btn').click()
    time.sleep(1)
    #driver.find_element####
    # driver.find_element(By.ID, 'mvideo-form-field-input-0').send_keys(NUMBER)
    # driver.find_element(By.LINK_TEXT, 'Продолжить').click()
    time.sleep(2)


def all_handler(driver):
    # tele2_handler(driver)
    # delivery_handler(driver)
    # hh_handler(driver)
    mvideo_handler(driver)


if __name__ == '__main__':
    driver = get_session()
    all_handler(driver)
