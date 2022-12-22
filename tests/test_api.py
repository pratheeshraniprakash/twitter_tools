"""Unit tests for API."""

from fastapi.testclient import TestClient

from app import app


client: TestClient = TestClient(app)


def test_scraping_0() -> None:
    """Test case for valid requests."""
    request_ = {
        "search_string": "BSNL"
    }
    response_ = client.post("/scrape", json=request_)
    assert response_.status_code == 200
    assert 'tweets' in response_.json().keys()
    assert 'users' in response_.json().keys()
    assert 'tweet_id' in response_.json()["tweets"].keys()
    assert 'tweet_text' in response_.json()["tweets"].keys()
    assert 'user_id' in response_.json()["tweets"].keys()
    assert 'conversation_id' in response_.json()["tweets"].keys()
    assert 'created_at' in response_.json()["tweets"].keys()
    assert 'lang' in response_.json()["tweets"].keys()
    assert 'like_count' in response_.json()["tweets"].keys()
    assert 'quote_count' in response_.json()["tweets"].keys()
    assert 'reply_count' in response_.json()["tweets"].keys()
    assert 'retweet_count' in response_.json()["tweets"].keys()
    assert 'possibly_sensitive' in response_.json()["tweets"].keys()


def test_scraping_1() -> None:
    """Test case for invalid request."""
    request_ = {
        "limit_tweets": 100
    }
    response_ = client.post("/scrape", json=request_)
    assert response_.status_code == 422


def test_analyse_0() -> None:
    """Test case for invalid request."""
    request_ = {
        "exclude_handles": ["@bsnl"]
    }
    response_ = client.post("/sentiment", json=request_)
    assert response_.status_code == 422
