"""Collect tweets."""
from typing import Dict, List

from database.database import Database
from database.models import DataBaseModel
from scrape.twitter import Response


def scrape(search_term: str) -> Dict[str, List[str]]:
    """Scrape tweets."""
    response: Response = Response(search_term)
    database_tables: DataBaseModel = DataBaseModel(response)
    tweet_dict: Dict[str, List[str]] = __get_tweet_dict(database_tables)
    return tweet_dict


def __get_tweet_dict(database_tables: DataBaseModel) -> Dict[str, List[str]]:
    """Convert processed response to Python dictionary."""
    return_dict:  Dict[str, List[str]] = {
        'tweet_id': [],
        'tweet_text': [],
        'author_id': [],
        'conversation_id': [],
        'created_at': [],
        'lang': [],
        'like_count': [],
        'quote_count': [],
        'reply_count': [],
        'retweet_count': [],
        'possibly_sensitive': [],
    }
    for tweet in database_tables.tweet_object_list:
        for _key in return_dict.keys():
            if _key == "created_at":
                return_dict[_key].append(tweet.__dict__[_key].strftime('%d-%m-%Y %H:%M:%S.%f %z %Z'))
            else:
                return_dict[_key].append(tweet.__dict__[_key])

    return return_dict


def database_write(database_model: DataBaseModel) -> None:
    """Write to databse."""
    database_: Database = Database(database_model.get_tables())
    database_.commit_data()
    print("Completed.")


if __name__ == '__main__':
    response = scrape("BSNL")
    database_write(response)
