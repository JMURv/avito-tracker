from addons.addons import get_session
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re


url = 'https://www.amazon.com/s?k=rtx+3080&i=electronics&bbn=284822&rh=n%3A284822%2Cp_n_feature_browse-bin%3A23883932011%2Cp_n_condition-type%3A2224371011%2Cp_72%3A1248879011%2Cp_36%3A10000-50000&s=price-asc-rank&dc&crid=B7CYC5WF6QOU&qid=1667578434&rnid=386442011&sprefix=%2Caps%2C233&ref=sr_nr_p_36_2'
# url = 'https://www.amazon.com/s?k=playstation+5&ref=nb_sb_noss'

def parse_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all("h2", {'class': 'a-size-mini a-spacing-none a-color-base s-line-clamp-2'}):
        name = link.findNext('a').findNext('span').text
        img = link.findNext('img', {'alt': name})
        href = f"https://amazon.com{link.findNext('a')['href']}"
        try:
            price = link.find("span", {'class': 'a-offscreen'}).text
        except(Exception):
            price = 'Price is hidden by Amazon'
        print(img)
        break


def amazon_parse(driver):
    driver.get(url)
    time.sleep(2)
    parse_content(driver.page_source)
    return


if __name__ == '__main__':
    driver = get_session()
    amazon_parse(driver)
    driver.quit()
