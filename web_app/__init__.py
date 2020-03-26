# web_app/__init__.py

from flask import Flask

from web_app.models import db, migrate
from web_app.routes.home_routes import home_routes
from web_app.routes.user_routes import user_routes
from web_app.routes.tweet_routes import tweet_routes
from web_app.routes.stats_routes import stats_routes
from web_app.routes.admin_routes import admin_routes

from dotenv import load_dotenv
import os

load_dotenv()


class Config:
    """ Base configuration reading from .env file """
    SECRET_KEY = os.environ.get("SECRET_KEY")


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///web_app.db'

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(home_routes)
    app.register_blueprint(tweet_routes)
    app.register_blueprint(user_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(stats_routes)

    return app


if __name__ == '__main__':
    my_app = create_app()
    my_app.secret_key = Config.SECRET_KEY
    my_app.config['SESSION_TYPE'] = 'filesystem'
    my_app.run(debug=True)
