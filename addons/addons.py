import time
from selenium import webdriver
from fake_useragent import UserAgent
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def allpage_load(driver):
    for _ in range(1, 7):
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
        if _ == 6:
            driver.execute_script(
                "window.scrollTo(0, 8200)"
            )
        time.sleep(0.5)


def get_session():
    options = Options()
    options.add_argument(f'user-agent={UserAgent().chrome}')
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")  # Silent Mode
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver
