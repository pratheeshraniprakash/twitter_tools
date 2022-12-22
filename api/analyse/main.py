"""Endpoints for sentiment analysis."""

from typing import Dict, List

from app import app

from api.analyse.schema import SentimentInput, SentimentOutput

from analysis.main import analyse


@app.post("/sentiment", response_model=SentimentOutput)
def analyse_(input: SentimentInput):
    """Estimate sentiments."""
    results: Dict[str, List[str]] = analyse(
        tweet_table=input.tweets,
        exclude_handles=input.exclude_handles,
        period=input.period
    )
    return {'tweets': results}
