from . import db, login_manager

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

"""Model for Cards."""
class Card(db.Model):
		__tablename__ = 'card'
		id = db.Column(db.Integer,primary_key=True)
		deck_name = db.Column(db.String)
		front = db.Column(db.String)
		back = db.Column(db.String)
		created_by =  db.Column(db.String, db.ForeignKey('deck.name'))


"""Model for Decks."""
class Deck(db.Model):
		__tablename__ = 'deck'
		id = db.Column(db.Integer,primary_key=True)
		name = db.Column(db.String, unique=True)
		summary = db.Column(db.String)
		created_by =  db.Column(db.String, db.ForeignKey('users.id'))
		cards = db.relationship('Card', backref = 'deck', lazy=True)

"""Model for Users."""
class User(UserMixin, db.Model):
		__tablename__ = 'users'
		id = db.Column(db.Integer,primary_key=True)
		username = db.Column(db.String, unique=True)
		password = db.Column(db.String)
		decks = db.relationship('Deck', backref = 'users')