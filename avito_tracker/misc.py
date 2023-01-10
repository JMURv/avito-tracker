import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

DB_ENV = {
    'user': os.getenv('USER'),
    'password': os.getenv('PASSWORD'),
    'host': os.getenv('HOST'),
    'port': os.getenv('PORT'),
    'database': os.getenv('DATABASE')
}

BOT_ENV = {
    'token': os.getenv('TOKEN'),
    'yoomoney_token': os.getenv('YOOMONEY_TOKEN')
}
