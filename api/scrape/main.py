"""Endpoints for scraping."""
from typing import Dict, List

from app import app

from api.scrape.schema import ScrapeInput, ScrapeOutput

from scrape.main import scrape


@app.post("/scrape", response_model=ScrapeOutput)
def scrape_(input: ScrapeInput):
    """Scrape tweets using Twitter api."""
    results: Dict[str, List[str]] = scrape(search_term=input.search_string)
    return {'tweets': results}
