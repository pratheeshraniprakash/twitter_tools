import base64
from dotenv import load_dotenv
import os
import requests
import time
from typing import List
import urllib


class AuthToken():
    """Generate OAuth2 token to authenticate with Twitter APIv2."""

    def __init__(self) -> None:
        self.AUTH_URL = "https://api.twitter.com/oauth2/token"
        self._bearer_token = self.__authenticate()

    def __encode_credentials(self):
        load_dotenv()
        _api_key = os.environ["API_KEY"]
        _api_secret = os.environ["API_SECRET"]
        url_encoded_string = ":".join(
            [
                urllib.parse.quote_plus(_api_key),
                urllib.parse.quote_plus(_api_secret)
            ]
        ).encode("ascii")
        return base64.b64encode(url_encoded_string).decode("ascii")

    def __authenticate(self):
        basic_auth_string = self.__encode_credentials()

        header = {
            "Authorization": f"Basic {basic_auth_string}",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        }

        body = {"grant_type": "client_credentials"}
        response = requests.post(self.AUTH_URL, headers=header, data=body)
        return response.json()["access_token"]

    def get_bearer_token(self):
        return self._bearer_token


class Request():
    """Request model."""

    def __init__(self, search_term, next_token=None, since_id=None):
        self.search_term = search_term
        self.next_token = next_token
        self.since_id = since_id
        self.expansions = "author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id,referenced_tweets.id,referenced_tweets.id.author_id"
        self.user_fields = "created_at,description,entities,id,location,name,pinned_tweet_id,profile_image_url,protected,public_metrics,url,username,verified,withheld"
        self.tweet_fields = "author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang,public_metrics,possibly_sensitive,referenced_tweets,reply_settings,source,text,withheld"
        self.place_fields = (
            "contained_within,country,country_code,full_name,geo,id,name,place_type"
        )
        self.MAX_RESULTS = 100
        self.request_header = self.__create_request_header()
        self.search_query = self.__create_search_query()

    def __create_request_header(self):
        bearer_token = AuthToken().get_bearer_token()
        request_header = {
            "Authorization": f"Bearer {bearer_token}",
            "Accept-Encoding": "gzip",
            "content-type": "application/json",
        }
        return request_header

    def __create_search_query(self):
        search_query = {
            "query": self.search_term,
            "expansions": self.expansions,
            "user.fields": self.user_fields,
            "tweet.fields": self.tweet_fields,
            "place.fields": self.place_fields,
            "max_results": self.MAX_RESULTS,
            "next_token": self.next_token,
            "since_id": self.since_id,
        }
        return search_query

    def get_request_header(self):
        return self.request_header

    def get_request_params(self):
        return self.search_query

    def get_next_token(self):
        return self.next_token


class Response():
    """CollectResponse model."""

    def __init__(self, search_term: str) -> None:
        self.SEARCH_TWEET_URL: str = "https://api.twitter.com/2/tweets/search/recent"
        self.search_term: str = search_term
        self.raw_data_list: List[dict] = []
        self.raw_includes_list: List[dict] = []
        self.limit_rate_available: int = 1
        self.limit_rate_reset_time: int = 1
        self.next_token = None
        self.since_id = None
        self.__get_response()

    def __get_response(self):
        while True:
            request_ = Request(
                self.search_term,
                self.next_token,
                self.since_id
            )
            response = requests.get(
                self.SEARCH_TWEET_URL,
                headers=request_.get_request_header(),
                params=request_.get_request_params(),
            )
            self.__process_data(response)
            print("Fetching data.")
            if response.status_code == 200:
                if self.__process_meta(response.json()["meta"]):
                    break
                self.__process_headers(response.headers)
            else:
                print(f"Failed with status code {response.status_code}")
                break

    def __process_meta(self, response_meta):
        if response_meta["result_count"] == 0:
            print("Fetched all tweets.")
            return True
        try:
            self.next_token = response_meta["next_token"]
        except KeyError:
            print("No more tokens.")
            return True

    def __process_headers(self, header):
        self.limit_rate_available = header["x-rate-limit-remaining"]
        if self.limit_rate_available == 0:
            self.limit_rate_reset_time = (
                int(header["x-rate-limit-reset"]) - time.time() + 1
            )
            print(f"Sleeping for {self.limit_rate_reset_time} seconds.")
            time.sleep(self.limit_rate_reset_time)

    def __process_data(self, response):
        data_ = response.json()["data"]
        includes_ = response.json()["includes"]
        self.raw_data_list += data_
        self.raw_includes_list.append(includes_)

    def get_raw_data_list(self):
        return self.raw_data_list

    def get_raw_includes_list(self):
        return self.raw_includes_list

    def get_search_term(self):
        return self.search_term
