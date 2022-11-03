import time
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def get_right_xpath(page):
    digit = 7
    if page >= 3:
        digit = 8
    if page >= 4:
        digit = 9
    return digit


def page_wait(driver):
    for _ in range(1, 6):
        if _ == 1:
            driver.execute_script(
                "window.scrollTo(0, 1800)"
            )

        if _ == 2:
            driver.execute_script(
                "window.scrollTo(0, 2800)"
            )

        if _ == 3:
            driver.execute_script(
                "window.scrollTo(0, 4200)"
            )

        if _ == 4:
            driver.execute_script(
                "window.scrollTo(0, 5800)"
            )

        if _ == 5:
            driver.execute_script(
                "window.scrollTo(0, 7200)"
            )
        time.sleep(0.5)


def get_session():
    options = Options()
    options.add_argument(f'user-agent={UserAgent().chrome}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver
