from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
import os
import pytest
from dotenv import load_dotenv


# test db stuff
load_dotenv()
username = os.getenv('POSTGRESQL_USER')
password = os.getenv('POSTGRESQL_PASSWORD')
dbname = os.getenv('DATABASE_NAME')
db_host = os.getenv('DB_HOST')
host_port = os.getenv('HOST_PORT')


connection_string = f"postgresql://{username}:{password}@{db_host}:{host_port}/{dbname}_test"
engine = create_engine(connection_string)
TestsessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base.metadata.create_all(bind=engine)

# def override_get_db():
#     db = TestsessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def session():
    # This will drop existing tables then create new ones, then it will return db session that can be used for querying

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestsessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)