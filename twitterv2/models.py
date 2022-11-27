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
        created_at: str,
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
