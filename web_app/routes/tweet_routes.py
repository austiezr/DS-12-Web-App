# web_app/routes/user_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect
from web_app.models import Tweet, User, parse_records, db
import web_app.twitter

tweet_routes = Blueprint('tweet_routes', __name__)


@tweet_routes.route('/tweets.json')
def list_tweets():
    print('VIEWED TWEETS JSON')
    tweets = Tweet.query.all()
    tweet_records = parse_records(tweets)
    return jsonify(tweet_records)


@tweet_routes.route('/tweets')
def list_tweets_for_humans():
    print('VIEWED TWEETS PAGE')
    tweets = Tweet.query.all()
    return render_template('tweets.html',
                           message='Here\'s some tweets!',
                           tweets=tweets)


@tweet_routes.route('/tweets/new')
def new_tweet():
    users = User.query.all()
    return render_template('new_tweet.html',
                           users=users)


@tweet_routes.route('/tweets/create', methods=['POST'])
def create_tweet():
    print('FORM DATA:', dict(request.form))
    created_tweet = Tweet(content=request.form['content'],
                          user_name=request.form['user_name'])
    db.session.add(created_tweet)
    db.session.commit()
    flash(f"Tweet by '{created_tweet.user_name}' created successfully!",
          "success")
    return redirect(f"/tweets")


@tweet_routes.route('/tweets/generate')
def gen_tweets():
    return render_template('tweet_gen.html')


@tweet_routes.route('/tweets/generated', methods=['POST'])
def get_tweets():
    print('FORM DATA:', dict(request.form))
    web_app.twitter.gen_tweets(q=request.form['q'],
                               count=request.form['count'],
                               since=request.form['since'])
    return redirect('/tweets')
