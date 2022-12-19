from urllib.parse import urlparse


async def url_validator(url):
    if type(url) is not str:
        return False
    if urlparse(url).netloc not in ('www.avito.ru', 'm.avito.ru'):
        return False
    return True
