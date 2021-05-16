db = {
    'user': 'hgjeon',
    'password': 'aaa369',
    'host': 'localhost',
    'port': 5432,
    'database': 'clean_solid_api'
}
DB_URL = f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"


test_db = {
    'user': 'hgjeon',
    'password': 'aaa369',
    'host': 'localhost',
    'port': 5432,
    'database': 'clean_solid_api'
}
test_config = {'DB_URL': f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}"}
