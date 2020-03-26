# web_app/routes/user_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect
from web_app.models import User, parse_records, db
import web_app.twitter

user_routes = Blueprint('user_routes', __name__)


@user_routes.route('/users.json')
def list_users():
    print('VIEWED USERS JSON')
    users = User.query.all()
    user_records = parse_records(users)
    return jsonify(user_records)


@user_routes.route('/users')
def list_users_for_humans():
    print('VIEWED USERS PAGE')
    users = User.query.all()
    return render_template('users.html',
                           message='Here\'s our users!',
                           users=users)


@user_routes.route('/users/new')
def new_user():
    return render_template('new_user.html')


@user_routes.route('/users/create', methods=['POST'])
def create_user():
    print('FORM DATA:', dict(request.form))
    created_user = User(name=request.form['name'])
    db.session.add(created_user)
    db.session.commit()
    flash(f"User '{created_user.name}' created successfully!", "success")
    return redirect("/users")


@user_routes.route('/users/get_user')
def get_user():
    return render_template('get_user.html')


@user_routes.route("/users/viewed_user", methods=['POST'])
def display_user(screen_name=None):
    screen_name = request.form['name']
    referenced_user = web_app.twitter.get_tweets(username=screen_name)
    return render_template('view_user.html',
                           username=referenced_user[0],
                           followers=referenced_user[1],
                           tmp=referenced_user[2])
