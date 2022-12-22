"""FastAPI server."""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from typing import Dict, List


tags_metadata: List[Dict[str, str]] = [
    {
        "name": "scrape",
        "description": "Scrape tweets.",
    },
    {
        "name": "estimate_sentiments",
        "description": "Estimate sentiment score.",
    },
]

app: FastAPI = FastAPI(
    debug=False,
    title="TweetSentiment Analysis",
    description="Endpoints for scraping tweets and sentiment analysis.",
    version="0.0.1",
    openapi_tags=tags_metadata,
)

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:5501",
    "http://localhost:5011",
    "http://127.0.0.1:5011",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    """Home route."""
    return {"message": "tweet sentiment analysis"}

from api.scrape.main import scrape_
from api.analyse.main import analyse_


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=5000)


# Sample 'n' number of tweets for a period of time. - Check for feasibility.
# Give the user the option to select period for resampling. ('H', 'D', )
