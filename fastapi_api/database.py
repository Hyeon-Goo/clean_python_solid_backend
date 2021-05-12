from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = {
    'user': 'hgjeon',
    'password': 'aaa369',
    'host': 'localhost',
    'port': 5432,
    'database': 'clean_solid_api'
}
DB_URL = f"postgresql://{db['user']}:{db['password']}@{db['host']}:{db['post']}/{db['database']}"

engine = create_engine(DB_URL, encoding='utf-8', max_overflow=0)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

