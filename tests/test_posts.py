import pytest
from typing import List
from app import schemas

def test_get_all_posts(client, test_posts):
    response = client.get("/posts/")
    posts = response.json()
    
    def validate(posts):
        return schemas.PostLikesResponse(**posts)
    
    posts_map = map(validate, posts)
    posts_list = list(posts_map)
    assert response.status_code == 200
    assert posts_list[0].likes == 0

def test_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostLikesResponse(**response.json())

    assert response.status_code == 200
    assert post.likes == 0
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert post.Post.author_info.id == test_posts[0].author

def get_non_existent_post(client, test_posts):
    response = client.get("/posts/12903")
    assert response.status_code == 404

@pytest.mark.parametrize("title, content, published", [
    ('Favorite MCU character', "Tony Stark", True),
    ('Favorite TV show', "Seal Team", True),
])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post("/posts/new", json={'title':title, 'content':content, 'published':published})
    created_post = schemas.PostResponse(**response.json())

    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.author_info.id == test_user['id']
    assert created_post.author_info.email == test_user['email']

def test_create_post_by_unauthenticated_user(client, test_user):
    response = client.post("/posts/new", json={'title':'title', 'content':'content', 'published':True})
    assert response.status_code == 401

@pytest.mark.parametrize("title, content",[
    ('Favorite MCU character', "Tony Stark"),
    ('Favorite TV show', "Seal Team"),
])
def test_default_post_published_value_as_true(authorized_client, test_user, title, content):
    response = authorized_client.post("/posts/new", json={'title':title, 'content':content})
    created_post = schemas.PostResponse(**response.json())

    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == True
    assert created_post.author_info.id == test_user['id']
    assert created_post.author_info.email == test_user['email']

def test_update_post_title(authorized_client, test_user, test_posts):
    response = authorized_client.put(f"/posts/{test_posts[0].id}/update", json={'title':"Updated post title"})
    updated_post = schemas.PostResponse(**response.json())

    assert updated_post.id == test_posts[0].id
    assert updated_post.title == 'Updated post title'
    assert updated_post.content == test_posts[0].content
    assert updated_post.published == test_posts[0].published
    assert updated_post.author_info.id == test_user['id']
    assert updated_post.author_info.email == test_user['email']

def test_update_post_content(authorized_client, test_user, test_posts):
    response = authorized_client.put(f"/posts/{test_posts[0].id}/update", json={'content':"Updated post content"})
    updated_post = schemas.PostResponse(**response.json())

    assert updated_post.id == test_posts[0].id
    assert updated_post.content == 'Updated post content'
    assert updated_post.title == test_posts[0].title
    assert updated_post.published == test_posts[0].published
    assert updated_post.author_info.id == test_user['id']
    assert updated_post.author_info.email == test_user['email']

def test_update_post_published(authorized_client, test_user, test_posts):
    response = authorized_client.put(f"/posts/{test_posts[0].id}/update", json={'published':False})
    updated_post = schemas.PostResponse(**response.json())
    assert updated_post.id == test_posts[0].id
    assert updated_post.title == test_posts[0].title
    assert updated_post.content == test_posts[0].content
    assert updated_post.published == False
    assert updated_post.author_info.id == test_user['id']
    assert updated_post.author_info.email == test_user['email']

def test_update_non_existent_post(authorized_client, test_user, test_posts):
    response = authorized_client.put(f"/posts/12/update", json={'published':False})
    assert response.status_code == 404

def test_update_post_by_unauthenticated_user(client, test_user, test_posts):
    response = client.put(f"/posts/{test_posts[0].id}/update", json={'published':False})
    assert response.status_code == 401

def test_update_other_users_post(authorized_client, test_user,test_user2, test_posts):
    response = authorized_client.put(f"/posts/{test_posts[4].id}/update", json={'title':"Trying to update another user's post"})
    assert response.status_code == 403

def test_delete_post_success(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}/delete")
    assert response.status_code == 204

def test_delete_non_existent_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f"/posts/12/delete")
    assert response.status_code == 404

def test_delete_post_by_unauthenticated_user(client, test_user, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}/delete")
    assert response.status_code == 401

def test_delete_other_users_post(authorized_client, test_user,test_user2, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[4].id}/delete")
    assert response.status_code == 403