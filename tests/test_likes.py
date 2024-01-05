import pytest
from app import schemas
from app import models


def test_user_likes(client, test_user, liked_posts,session):
    response = client.get(f"/likes/{test_user['id']}")
    user_liked_posts = [schemas.PostResponse(**post) for post in response.json()]

    for liked_post in user_liked_posts:
        like = session.query(models.Like).filter(models.Post.id == liked_post.id).first()
        assert like.user_id == test_user['id']
    

def test_like_post(authorized_client, test_user, test_posts):
    response = authorized_client.post(f"/likes/{test_posts[4].id}/like")
    assert response.status_code == 201

    
def test_like_post_by_unauthenticated_user(client, test_user, test_posts):
    response = client.post(f"/likes/{test_posts[4].id}/like")
    assert response.status_code == 401