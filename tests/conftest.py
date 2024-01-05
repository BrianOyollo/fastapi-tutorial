from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base
from app import oauth2
from app import models
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


connection_string = f"postgresql://postgres:TestPassword5432@localhost:5432/fastapidb_test"
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


@pytest.fixture
def test_user(client):
    test_user_data = {"email":"jasonhayes@gmail.com", "password":"Testpass123"}
    response = client.post("/users/new", json=test_user_data)
    test_user = response.json()
    test_user['password'] = test_user_data['password']
    return test_user

@pytest.fixture
def test_user2(client):
    test_user_data = {"email":"rayperry@gmail.com", "password":"Testpass123"}
    response = client.post("/users/new", json=test_user_data)
    test_user = response.json()
    test_user['password'] = test_user_data['password']
    return test_user


@pytest.fixture
def token(test_user):
    return oauth2.create_access_token(data = {'user_id':test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers, 
        "Authorization": f"Bearer {token}"

    }
    return client

@pytest.fixture
def test_posts(test_user,test_user2, session):
    """
    Adds dummy posts in the testing db
    """
    dummy_posts = [

        {
            'title':"Test post 1",
            'content': 'Contents of test post 1',
            'author': test_user['id']
        },
        {
            'title':"Test post 2",
            'content': 'Contents of test post 2',
            'author': test_user['id']
        },
        {
            'title':"Test post 3",
            'content': 'Contents of test post 3',
            'author': test_user['id']
        },
        {
            'title':"Test post 4",
            'content': 'Contents of test post 4',
            'author': test_user['id']
        },
        {
            'title':"Test post 5",
            'content': 'Contents of test post 5',
            'author': test_user2['id']
        }
    ]

    def create_post_model(post):
        return models.Post(**post)
    
    posts_map = map(create_post_model, dummy_posts)
    posts_list = list(posts_map)

    session.add_all(posts_list)
    session.commit()

    db_posts = session.query(models.Post).all()
    return db_posts


@pytest.fixture
def liked_posts(authorized_client, test_user, test_posts):
    response = authorized_client.post(f"/likes/{test_posts[4].id}/like")
    return response
    