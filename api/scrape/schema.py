"""Input/Output schema for /scrape endpoint."""

from pydantic import BaseModel
from typing import Dict, List, Optional


class ScrapeInput(BaseModel):
    """API model for Scrape input."""

    search_string: str
    date_range: Optional[str]
    exclude_handles: Optional[List[str]]
    limit_tweets: Optional[int]


class ScrapeOutput(BaseModel):
    """API model for Scrape output."""

    tweets: Dict[str, List[str]]
    users: Dict[str, List[str]]
    # context_annotations: Dict[str, List[str]]
    # referenced_tweets: Dict[str, List[str]]
    # tweet_entity_annotations: Dict[str, List[str]]
    # tweet_entity_hashtags: Dict[str, List[str]]
    # tweet_entity_mentions: Dict[str, List[str]]
    # tweet_entity_urls: Dict[str, List[str]]
    # user_description_hashtags: Dict[str, List[str]]
    # user_description_mentions: Dict[str, List[str]]
    # user_description_url: Dict[str, List[str]]
