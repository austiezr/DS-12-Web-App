from flask import Blueprint, jsonify, request, render_template, flash, redirect

from web_app.models import db
from web_app.twitter import get_tweets

admin_routes = Blueprint('admin_routes', __name__)


@admin_routes.route("/admin/db/reset")
def reset_db():
    print(type(db))
    db.drop_all()
    db.create_all()
    return jsonify({'message': 'DB RESET OK'})


@admin_routes.route('/admin/db/seed')
def seed_db():
    print(type(db))
    default_users = ['elonmusk', 'austen', 'nbcnews', 'austieziech']
    for screen_name in default_users:
        get_tweets(screen_name)

    return jsonify({'message': f'DB SEEDED OK (w/ {len(default_users)}'})
