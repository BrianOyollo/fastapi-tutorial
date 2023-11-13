from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

username = os.environ['POSTGRESQL_USER']
password = os.environ['POSTGRESQL_PASSWORD']
dbname = 'fastapidb'


connection_string = f"postgresql://{username}:{password}@localhost/{dbname}"
engine = create_engine(connection_string)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
