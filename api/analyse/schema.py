"""Input/Output schema for /sentiment endpoint."""

from pydantic import BaseModel
from typing import Dict, List, Optional


class SentimentInput(BaseModel):
    """API model for Sentiment input."""

    tweets: Dict[str, List[str]]
    exclude_handles: Optional[List[str]]
    period: Optional[str] = 'day'
    multi_language: bool = True


class SentimentOutput(BaseModel):
    """API model for Sentiment output."""

    tweet_sentiment_table: Dict[str, List[str]]
    sentiment_table_1: Dict[str, List[str]]
    sentiment_table_2: Dict[str, List[str]]
