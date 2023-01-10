from avito_tracker.misc import DB_ENV

user = DB_ENV.get('user')
password = DB_ENV.get('password')
host = DB_ENV.get('host')
port = DB_ENV.get('port')
database = DB_ENV.get('database')

DSN = f"postgres://{user}:{password}@{host}:{port}/{database}"
