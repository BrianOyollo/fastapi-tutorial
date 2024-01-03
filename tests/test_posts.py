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

def test_get_all_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostLikesResponse(**response.json())

    assert response.status_code == 200
    assert post.likes == 0
    assert post.Post.id == test_posts[0].id
    assert post.Post.author_info.id == test_posts[0].author