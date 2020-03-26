from flask import Blueprint, request, jsonify, render_template
from sklearn.linear_model import LogisticRegression
from web_app.models import User, Tweet
import basilica
import os

BASILICA = basilica.Connection(os.getenv('BASILICA_KEY'))

stats_routes = Blueprint('stats_routes', __name__)


@stats_routes.route('/stats/prepare')
def prepare():
    print('Im here')
    users = User.query.all()
    return render_template('prepare_to_predict.html',
                           users=users)


@stats_routes.route('/stats/predict', methods=['POST'])
def predict():
    print('PREDICT ROUTE...')
    print('FORM DATA:', dict(request.form))
    screen_name_a = request.form['screen_name_a']
    screen_name_b = request.form['screen_name_b']
    tweet_text = request.form['text']

    user_a = User.query.filter(User.name == screen_name_a).one()
    user_b = User.query.filter(User.name == screen_name_b).one()
    user_a_tweets = user_a.tweets
    user_b_tweets = user_b.tweets

    embedding = []
    labels = []
    for tweet in user_a_tweets:
        labels.append(user_a.name)
        embedding.append(tweet.embeddings)

    for tweet in user_b_tweets:
        labels.append(user_b.name)
        embedding.append(tweet.embeddings)
    breakpoint()
    classifier = LogisticRegression()
    classifier.fit(embedding, labels)

    example_embedding = BASILICA.embed_sentence(tweet_text)
    result = classifier.predict([example_embedding])
    return render_template('results.html',
                           screen_name_a=screen_name_a,
                           screen_name_b=screen_name_b,
                           tweet_text=tweet_text,
                           screen_name_most_likely=result[0])
