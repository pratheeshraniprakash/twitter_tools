import datetime
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    Boolean,
    Float,
    ForeignKey,
    UnicodeText,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from typing import List

from scrape.twitter import Response

Base = declarative_base()


class Tweet(Base):
    __tablename__: str = "tweet_table"

    tweet_id = Column("tweet_id", UnicodeText, primary_key=True)
    author_id = Column("author_id", UnicodeText, ForeignKey("users.user_id"))
    created_at = Column("created_at", DateTime)
    reply_settings = Column("reply_settings", UnicodeText)
    tweet_text = Column("tweet_text", UnicodeText)
    conversation_id = Column("conversation_id", UnicodeText)
    possibly_sensitive = Column("possibly_sensitive", Boolean)
    retweet_count = Column("retweet_count", Integer)
    reply_count = Column("reply_count", Integer)
    like_count = Column("like_count", Integer)
    quote_count = Column("quote_count", Integer)
    lang = Column("lang", UnicodeText)
    source = Column("source", UnicodeText)
    search_term = Column("search_term", UnicodeText)
    referenced_tweets = relationship("ReferencedTweet")
    context_annotation = relationship("ContextAnnotations")
    tweet_entity_urls = relationship("TweetEntity_URL")
    tweet_entity_mentions = relationship("TweetEntity_Mentions")
    tweet_entity_hashtags = relationship("TweetEntity_Hashtags")
    tweet_entity_annotations = relationship("TweetEntity_Annotations")

    def __init__(
        self,
        author_id: str,
        tweet_id: str,
        created_at: datetime.datetime,
        reply_settings: str,
        tweet_text: str,
        conversation_id: str,
        possibly_sensitive: bool,
        retweet_count: int,
        reply_count: int,
        like_count: int,
        quote_count: int,
        lang: str,
        source: str,
        search_term: str
    ) -> None:
        self.author_id = author_id
        self.tweet_id = tweet_id
        self.created_at = created_at
        self.reply_settings = reply_settings
        self.tweet_text = tweet_text
        self.conversation_id = conversation_id
        self.possibly_sensitive = possibly_sensitive
        self.retweet_count = retweet_count
        self.reply_count = reply_count
        self.like_count = like_count
        self.quote_count = quote_count
        self.lang = lang
        self.source = source
        self.search_term = search_term


class ReferencedTweet(Base):
    __tablename__ = "referenced_tweet_table"

    id_ = Column("id_", Integer, primary_key=True, autoincrement=True)
    originating_tweet_id = Column(
        "originating_tweet_id", UnicodeText, ForeignKey("tweet_table.tweet_id")
    )
    referenced_tweet_id = Column("referenced_tweet_id", UnicodeText)
    referencing_type = Column("referencing_type", UnicodeText)

    def __init__(
        self, tweet_id: str, referenced_tweet_id: str, referencing_type: str
    ) -> None:
        self.originating_tweet_id = tweet_id
        self.referenced_tweet_id = referenced_tweet_id
        self.referencing_type = referencing_type


class ContextAnnotations(Base):
    __tablename__ = "context_annotations"

    id_ = Column("id_", Integer, primary_key=True, autoincrement=True)
    originating_tweet_id = Column(
        "originating_tweet_id", UnicodeText, ForeignKey("tweet_table.tweet_id")
    )
    annotation_id = Column("annotation_id", UnicodeText)
    annotation_name = Column("annotation_name", UnicodeText)
    annotation_description = Column("annotation_description", UnicodeText)
    annotation_entity_id = Column("annotation_entity_id", UnicodeText)
    annotation_entity_name = Column("annotation_entity_name", UnicodeText)

    def __init__(
        self,
        tweet_id: str,
        annotation_id: str,
        annotation_name: str,
        annotation_description: str,
        annotation_entity_id: str,
        annotation_entity_name: str,
    ) -> None:
        self.originating_tweet_id = tweet_id
        self.annotation_id = annotation_id
        self.annotation_name = annotation_name
        self.annotation_description = annotation_description
        self.annotation_entity_id = annotation_entity_id
        self.annotation_entity_name = annotation_entity_name


class TweetEntity_URL(Base):
    __tablename__ = "tweet_entity_urls"

    id_ = Column("id_", Integer, primary_key=True, autoincrement=True)
    originating_tweet_id = Column(
        "originating_tweet_id", UnicodeText, ForeignKey("tweet_table.tweet_id")
    )
    url = Column("url", UnicodeText)
    url_status = Column("url_status", Integer)
    url_title = Column("url_title", UnicodeText)
    url_description = Column("url_description", UnicodeText)

    def __init__(
        self,
        tweet_id: str,
        url: str,
        url_status=None,
        url_title=None,
        url_description=None,
    ) -> None:
        self.originating_tweet_id = tweet_id
        self.url = url
        self.url_status = url_status
        self.url_title = url_title
        self.url_description = url_description


class TweetEntity_Mentions(Base):
    __tablename__ = "tweet_entity_mentions"

    id_ = Column("id_", Integer, primary_key=True, autoincrement=True)
    originating_tweet_id = Column(
        "originating_tweet_id", UnicodeText, ForeignKey("tweet_table.tweet_id")
    )
    mentioned_username = Column(
        "mentioned_username",
        UnicodeText,
        ForeignKey("users.user_id")
    )
    mentioned_user_id = Column("mentioned_user_id", UnicodeText)

    def __init__(self, tweet_id: str, username: str, user_id: str) -> None:
        self.originating_tweet_id = tweet_id
        self.mentioned_username = username
        self.mentioned_user_id = user_id


class TweetEntity_Hashtags(Base):
    __tablename__ = "tweet_entity_hashtags"

    id_ = Column("id_", Integer, primary_key=True, autoincrement=True)
    originating_tweet_id = Column(
        "originating_tweet_id", UnicodeText, ForeignKey("tweet_table.tweet_id")
    )
    hashtag = Column("hashtag", UnicodeText)

    def __init__(self, tweet_id, hashtag: str) -> None:
        self.originating_tweet_id = tweet_id
        self.hashtag = hashtag


class TweetEntity_Annotations(Base):
    __tablename__ = "tweet_entity_annotations"

    id_ = Column("id_", Integer, primary_key=True, autoincrement=True)
    originating_tweet_id = Column(
        "originating_tweet_id", UnicodeText, ForeignKey("tweet_table.tweet_id")
    )
    annotation_normalised_text = Column("annotation_normalised_text", UnicodeText)
    annotation_type = Column("annotation_type", UnicodeText)
    annotation_probability = Column("annotation_probability", Float)

    def __init__(
        self,
        tweet_id: str,
        annotation_type: str,
        annotation_probability: float,
        annotation_text: str,
    ) -> None:
        self.originating_tweet_id = tweet_id
        self.annotation_type = annotation_type
        self.annotation_probability = annotation_probability
        self.annotation_normalised_text = annotation_text


class User(Base):
    __tablename__ = "users"

    id_ = Column("id_", Integer, primary_key=True, autoincrement=True)
    user_id = Column("user_id", UnicodeText, unique=True)
    display_name = Column("display_name", UnicodeText)
    username = Column("username", UnicodeText)
    created_at = Column("created_at", DateTime)
    user_description = Column("user_description", UnicodeText)
    location = Column("location", UnicodeText)
    pinned_tweet_id = Column("pinned_tweet_id", UnicodeText)
    profile_image_url = Column("profile_image_url", UnicodeText)
    protected = Column("protected", Boolean)
    followers = Column("followers", Integer)
    following = Column("following", Integer)
    number_of_tweets = Column("number_of_tweets", Integer)
    listed_count = Column("listed_count", Integer)
    profile_url = Column("profile_url", UnicodeText)
    verified = Column("verified", Boolean)
    user_description_url = relationship("UserDescription_URL")
    user_description_hashtag = relationship("UserDescription_hashtag")
    user_description_mention = relationship("UserDescription_mention")
    tweet_table = relationship("Tweet")
    mentions = relationship("TweetEntity_Mentions")

    def __init__(
        self,
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
    ):
        self.user_id = user_id
        self.display_name = display_name
        self.username = username
        self.created_at = created_at
        self.user_description = user_description
        self.location = location
        self.pinned_tweet_id = pinned_tweet_id
        self.profile_image_url = profile_image_url
        self.protected = protected
        self.followers = followers
        self.following = following
        self.number_of_tweets = number_of_tweets
        self.listed_count = listed_count
        self.profile_url = profile_url
        self.verified = verified


class UserDescription_URL(Base):
    __tablename__ = "user_description_url"

    id_ = Column("id_", Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        "user_id", UnicodeText, ForeignKey("users.user_id")
    )
    url = Column("url", UnicodeText)

    def __init__(self, user_id, url):
        self.user_id = user_id
        self.url = url


class UserDescription_hashtag(Base):
    __tablename__ = "user_description_hashtags"

    id_ = Column("id_", Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        "user_id", UnicodeText, ForeignKey("users.user_id")
    )
    hashtag = Column("hashtag", UnicodeText)

    def __init__(self, user_id, hashtag):
        self.user_id = user_id
        self.hashtag = hashtag


class UserDescription_mention(Base):
    __tablename__ = "user_description_mentions"

    id_ = Column("id_", Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        "user_id", UnicodeText, ForeignKey("users.user_id")
    )
    mention = Column("mention", UnicodeText)

    def __init__(self, user_id, mention):
        self.user_id = user_id
        self.mention = mention


class DataBaseModel():
    """DataBaseModel class."""

    def __init__(self, response_object: Response) -> None:
        self.response_object = response_object
        self.raw_data = response_object.get_raw_data_list()
        self.raw_includes = response_object.get_raw_includes_list()
        self.search_term = response_object.get_search_term()
        self.tweet_object_list: List[Tweet] = []
        self.referenced_tweet_list: List[ReferencedTweet] = []
        self.context_annotations_list: List[ContextAnnotations] = []
        self.te_url_list: List[TweetEntity_URL] = []
        self.te_mention_list: List[TweetEntity_Mentions] = []
        self.te_hashtags_list: List[TweetEntity_Hashtags] = []
        self.te_annotations_list: List[TweetEntity_Annotations] = []
        self.user_list: List[User] = []
        self.user_url_object_list: List[UserDescription_URL] = []
        self.user_hashtag_list: List[UserDescription_hashtag] = []
        self.user_mention_list: List[UserDescription_mention] = []
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
            source = tweet_object.get("source")
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
                        url_status = item_.get("status")
                        url_title = item_.get("title")
                        url_description = item_.get("description")
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
                            item_.get("normalized_text"),
                            item_.get("type"),
                            item_.get("probability"),
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
                    user_description = user.get('description')
                    location = user.get('location')
                    pinned_tweet_id = user.get('pinned_tweet_id')
                    profile_image_url = user.get('profile_image_url')
                    protected = user.get('protected')
                    followers = user['public_metrics']['followers_count']
                    following = user['public_metrics']['following_count']
                    number_of_tweets = user['public_metrics']['tweet_count']
                    listed_count = user['public_metrics']['listed_count']
                    profile_url = user.get('url', '')
                    verified = user.get('verified')
                    unique_users = self.unique.get_user_id_list()
                    if not (user_id in unique_users):
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
    """UniqueKeys model."""

    def __init__(self):
        self.tweet_id_list: List[str] = []
        self.author_id_list: List[str] = []

    def get_tweet_id_list(self):
        return (self.tweet_id_list)

    def get_user_id_list(self):
        return (self.author_id_list)

    def add_tweet_id(self, tweet_id):
        self.tweet_id_list.append(tweet_id)

    def add_user_id(self, author_id):
        self.author_id_list.append(author_id)
