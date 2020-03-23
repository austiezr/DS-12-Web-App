# web_app/routes/home_routes.py

from flask import Blueprint, render_template

home_routes = Blueprint('home_routes', __name__)


@home_routes.route('/')
def home():
    return render_template('layout.html',
                           message='Welcome to TwitOff!')


@home_routes.route('/about')
def about():
    return "About Me!"
