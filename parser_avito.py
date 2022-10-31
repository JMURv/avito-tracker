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
