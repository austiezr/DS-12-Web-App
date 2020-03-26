# web_app/models.py

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
import basilica
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BASILICA_API_KEY')

connection = basilica.Connection(API_KEY)

db = SQLAlchemy()

migrate = Migrate()


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return '<User {}'.format(self.name)


class Tweet(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    timestamp = db.Column(db.TIMESTAMP, index=True, default=datetime.utcnow)
    content = db.Column(db.Unicode(280))
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))
    embeddings = db.Column(db.PickleType, nullable=False)

    def __repr__(self):
        return '<Tweet {}'.format(self.content)


def parse_records(database_records):
    """
    Parses database records into a clean json-like structure

    Param: database_records (a list of db.Model instances)

    Example: parse_records(User.query.all())

    Returns: a list of dictionaries, each corresponding to a record, like...

        [
            {"id": 1, "title": "Book 1"},
            {"id": 2, "title": "Book 2"},
            {"id": 3, "title": "Book 3"},
        ]

    """
    parsed_records = []
    for record in database_records:
        print(record)
        parsed_record = record.__dict__
        del parsed_record["_sa_instance_state"]
        parsed_records.append(parsed_record)
    return parsed_records
