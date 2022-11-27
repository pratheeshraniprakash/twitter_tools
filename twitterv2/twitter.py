import datetime
import requests
import time
import base64
import os
import urllib

from dotenv import load_dotenv
from models import (
    Tweet,
    ReferencedTweet,
    ContextAnnotations,
    TweetEntity_URL,
    TweetEntity_Mentions,
    TweetEntity_Hashtags,
    TweetEntity_Annotations,
    User,
    UserDescription_URL,
    UserDescription_hashtag,
    UserDescription_mention
)


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


class CollectResponse():
    def __init__(self, search_term):
        self.SEARCH_TWEET_URL = "https://api.twitter.com/2/tweets/search/recent"
        self.search_term = search_term
        self.raw_data_list = []
        self.raw_includes_list = []
        self.limit_rate_available = 1
        self.limit_rate_reset_time = 1
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
            # print(f"Fetching data.")
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


class ProcessedResponse():
    def __init__(self, response_object) -> None:
        self.response_object = response_object
        self.raw_data = response_object.get_raw_data_list()
        self.raw_includes = response_object.get_raw_includes_list()
        self.search_term = response_object.get_search_term()
        self.tweet_object_list = []
        self.referenced_tweet_list = []
        self.context_annotations_list = []
        self.te_url_list = []
        self.te_mention_list = []
        self.te_hashtags_list = []
        self.te_annotations_list = []
        self.user_list = []
        self.user_url_object_list = []
        self.user_hashtag_list = []
        self.user_mention_list = []
        self.unique = UniqueKeys()
        self.process_tweet_data()
        self.process_includes_data()

    def process_tweet_data(self) -> None:
        tweet_objects = self.raw_data
        for tweet_object in tweet_objects:
            author_id = tweet_object["author_id"]
            tweet_id = tweet_object["id"]
            created_at = datetime.datetime.strptime(
                tweet_object["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z"
            ).astimezone()
            reply_settings = tweet_object["reply_settings"]
            tweet_text = tweet_object["text"]
            conversation_id = tweet_object["conversation_id"]
            possibly_sensitive = tweet_object["possibly_sensitive"]
            retweet_count = int(
                tweet_object["public_metrics"]["retweet_count"]
            )
            reply_count = int(tweet_object["public_metrics"]["reply_count"])
            like_count = int(tweet_object["public_metrics"]["like_count"])
            quote_count = int(tweet_object["public_metrics"]["quote_count"])
            lang = tweet_object["lang"]
            source = tweet_object["source"]
            tweet = Tweet(
                author_id,
                tweet_id,
                created_at,
                reply_settings,
                tweet_text,
                conversation_id,
                possibly_sensitive,
                retweet_count,
                reply_count,
                like_count,
                quote_count,
                lang,
                source,
                self.search_term
            )
            self.tweet_object_list.append(tweet)

            if "referenced_tweets" in tweet_object.keys():
                for item_ in tweet_object["referenced_tweets"]:
                    referencing_type = item_["type"]
                    referencing_id = item_["id"]
                    rt = ReferencedTweet(
                        tweet_id,
                        referencing_id,
                        referencing_type
                    )
                    self.referenced_tweet_list.append(rt)

            if "context_annotations" in tweet_object.keys():
                for item_ in tweet_object["context_annotations"]:
                    annotation_id = item_["domain"]["id"]
                    annotation_name = item_["domain"]["name"]
                    try:
                        annotation_description = item_["domain"]["description"]
                    except KeyError:
                        annotation_description = None
                    annotation_entity_id = item_["entity"]["id"]
                    annotation_entity_name = item_["entity"]["name"]
                    ca = ContextAnnotations(
                        tweet_id,
                        annotation_id,
                        annotation_name,
                        annotation_description,
                        annotation_entity_id,
                        annotation_entity_name,
                    )
                    self.context_annotations_list.append(ca)

            if "entities" in tweet_object.keys():
                if "urls" in tweet_object["entities"]:
                    for item_ in tweet_object["entities"]["urls"]:
                        try:
                            url_status = item_["status"]
                        except KeyError:
                            url_status = None
                        try:
                            url_title = item_["title"]
                        except KeyError:
                            url_title = None
                        try:
                            url_description = item_["description"]
                        except KeyError:
                            url_description = None
                        te_url = TweetEntity_URL(
                            tweet_id,
                            item_["expanded_url"],
                            url_status,
                            url_title,
                            url_description,
                        )
                        self.te_url_list.append(te_url)

                if "mentions" in tweet_object.keys():
                    for item_ in tweet_object["mentions"]:
                        te_mention = TweetEntity_Mentions(
                            tweet_id, item_['username'], item_["id"]
                        )
                        self.te_mention_list.append(te_mention)

                if "hashtags" in tweet_object.keys():
                    for item_ in tweet_object["hashtags"]:
                        te_hashtag = TweetEntity_Hashtags(
                            tweet_id, item_["tag"]
                        )
                        self.te_hashtags_list.append(te_hashtag)

                if "annotations" in tweet_object.keys():
                    for item_ in tweet_object["annotations"]:
                        te_annotation = TweetEntity_Annotations(
                            tweet_id,
                            item_["normalized_text"],
                            item_["type"],
                            item_["probability"],
                        )
                        self.te_annotations_list.append(te_annotation)

    def process_includes_data(self):
        includes = self.raw_includes
        for item_ in includes:
            if 'users' in item_.keys():
                for user in item_['users']:
                    user_id = user['id']
                    display_name = user['name']
                    username = user['username']
                    created_at = datetime.datetime.strptime(
                        user['created_at'],
                        "%Y-%m-%dT%H:%M:%S.%f%z"
                    ).astimezone()
                    user_description = user['description']
                    if 'location' in user.keys():
                        location = user['location']
                    else:
                        location = None
                    if 'pinned_tweet_id' in user.keys():
                        pinned_tweet_id = user['pinned_tweet_id']
                    else:
                        pinned_tweet_id = None
                    profile_image_url = user['profile_image_url']
                    protected = user['protected']
                    followers = user['public_metrics']['followers_count']
                    following = user['public_metrics']['following_count']
                    number_of_tweets = user['public_metrics']['tweet_count']
                    listed_count = user['public_metrics']['listed_count']
                    profile_url = user['url']
                    verified = user['verified']
                    unique_users = self.unique.get_user_id_list()
                    if not(user_id in unique_users):
                        user_object = User(
                                    user_id,
                                    display_name,
                                    username,
                                    created_at,
                                    user_description,
                                    location,
                                    pinned_tweet_id,
                                    profile_image_url,
                                    protected,
                                    followers,
                                    following,
                                    number_of_tweets,
                                    listed_count,
                                    profile_url,
                                    verified
                        )
                        self.user_list.append(user_object)
                        self.unique.add_user_id(user_id)
                    else:
                        pass
                    if 'entities' in user.keys():
                        if 'url' in user['entities']:
                            for url_dict in user['entities']['url']['urls']:
                                if 'expanded_url' in url_dict.keys():
                                    url = url_dict['expanded_url']
                                else:
                                    url = url_dict['url']
                                url_object = UserDescription_URL(user_id, url)
                                self.user_url_object_list.append(url_object)
                        if 'description' in user['entities']:
                            if 'hashtags' in user['entities']['description'].keys():
                                for hashtag_dict in user['entities']['description']['hashtags']:
                                    hashtag = hashtag_dict['tag']
                                    hashtag_object = UserDescription_hashtag(user_id, hashtag)
                                    self.user_hashtag_list.append(hashtag_object)
                            if 'mentions' in user['entities']['description']:
                                for mention_dict in user['entities']['description']['mentions']:
                                    mention = mention_dict['username']
                                    mention_object = UserDescription_mention(user_id, mention)
                                    self.user_mention_list.append(mention_object)

    def get_tables(self):
        object_lists = [
            self.user_list,
            self.tweet_object_list,
            self.referenced_tweet_list,
            self.context_annotations_list,
            self.te_url_list,
            self.te_mention_list,
            self.te_hashtags_list,
            self.te_annotations_list,
            self.user_url_object_list,
            self.user_hashtag_list,
            self.user_mention_list,
        ]
        return object_lists


class UniqueKeys():
    def __init__(self):
        self.tweet_id_list = []
        self.author_id_list = []

    def get_tweet_id_list(self):
        return (self.tweet_id_list)

    def get_user_id_list(self):
        return (self.author_id_list)

    def add_tweet_id(self, tweet_id):
        self.tweet_id_list.append(tweet_id)

    def add_user_id(self, author_id):
        self.author_id_list.append(author_id)
