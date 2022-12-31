from urllib.parse import urlparse


async def url_validator(url: str) -> bool:
    if type(url) is not str:
        return False
    if urlparse(url).netloc not in ('www.avito.ru', 'm.avito.ru'):
        return False
    return True


async def payment_validator(worker_quantity: str, days: str) -> bool:
    if worker_quantity.isdigit() and days.isdigit():
        if worker_quantity in ('5', '10', '15'):
            return True
    return False
