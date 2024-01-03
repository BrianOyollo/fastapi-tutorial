from sqlalchemy import create_engine

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


load_dotenv()
username = os.getenv('POSTGRESQL_USER')
password = os.getenv('POSTGRESQL_PASSWORD')
dbname = os.getenv('DATABASE_NAME')
db_host = os.getenv('DB_HOST')
host_port = os.getenv('HOST_PORT')


connection_string = f"postgresql://{username}:{password}@{db_host}:{host_port}/{dbname}"
engine = create_engine(connection_string)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
