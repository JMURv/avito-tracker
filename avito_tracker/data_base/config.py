import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
user = os.getenv('user')
password = os.getenv('password')
host = os.getenv('host')
port = os.getenv('port')
database = os.getenv('database')

DSN = f"postgres://{user}:{password}@{host}:{port}/{database}"
