from urllib.parse import urlparse


async def url_validator(url: str) -> bool:
    if type(url) is not str:
        return False
    if urlparse(url).netloc not in ('www.avito.ru', 'm.avito.ru'):
        return False
    return True


async def payment_validator(how_many: str, how_long: str) -> bool:
    if how_many.isdigit() and how_long.isdigit():
        if how_many in ('5', '10', '15'):
            return True
    return False
