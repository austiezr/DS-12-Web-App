# web_app/routes/user_routes.py

from flask import Blueprint, jsonify, request, render_template, flash, redirect
from web_app.models import User, parse_records, db

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
    created_user = User(name=request.form['name'],
                        birthdate=request.form['birthdate'],
                        dogs_cats=request.form['dog_or_cat'])
    db.session.add(created_user)
    db.session.commit()
    flash(f"User '{created_user.name}' created successfully!", "success")
    return redirect(f"/users")
