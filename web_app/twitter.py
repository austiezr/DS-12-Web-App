import os
from dotenv import load_dotenv
import basilica
import tweepy
from sqlalchemy import exc
import time
from web_app.models import db, Tweet, User

API_KEY = os.getenv('BASILICA_API_KEY')

connection = basilica.Connection(API_KEY)

load_dotenv()

TWITTER_AUTH = tweepy.OAuthHandler(
    os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET')
)

TWITTER_AUTH.set_access_token(
    os.getenv('TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
)

TWITTER = tweepy.API(TWITTER_AUTH)


def gen_tweets(q='#lambdaschool',
               count=100,
               ang='en',
               since='2019-10-21'):
    for tweet in tweepy.Cursor(TWITTER.search,
                               q=q,
                               count=count,
                               ang=ang,
                               since=since,
                               tweet_mode='extended').items():
        created_tweet = Tweet(id=tweet.id,
                              timestamp=tweet.created_at,
                              content=tweet.full_text,
                              user_id=tweet.user.id,
                              embeddings=connection.embed_sentence(
                                  tweet.full_text, model='twitter'))
        referenced_user = User(id=tweet.user.id,
                               name=tweet.user.screen_name)
        try:
            db.session.add(created_tweet)
            db.session.add(referenced_user)
            db.session.commit()
        except exc.IntegrityError:
            try:
                db.session.rollback()
                db.session.add(created_tweet)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                db.session.commit()
        time.sleep(2)


def get_tweets(username):
    user = TWITTER.get_user(username)
    statuses = TWITTER.user_timeline(username, tweet_mode="extended",
                                     count=150)
    tmp = []
    referenced_user = User(id=user.id,
                           name=user.screen_name)
    try:
        db.session.add(referenced_user)
        db.session.commit()
    except exc.IntegrityError:
        db.session.rollback()
        db.session.commit()
    for tweet in statuses:
        created_tweet = Tweet(id=tweet.id,
                              timestamp=tweet.created_at,
                              content=tweet.full_text,
                              user_id=tweet.user.id,
                              embeddings=connection.embed_sentence(
                                  tweet.full_text, model='twitter'
                              ))
        try:
            db.session.add(created_tweet)
            db.session.commit()
        except exc.IntegrityError:
            db.session.rollback()
            db.session.commit()
    for tweet in statuses:
        tmp.append(tweet.full_text)
    username = user.screen_name
    followers = user.followers_count
    return username, followers, tmp
