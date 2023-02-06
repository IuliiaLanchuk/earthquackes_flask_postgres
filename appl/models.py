from flask_sqlalchemy import SQLAlchemy

from appl.app import db


class Saver:
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model, Saver):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    city = db.Column(db.String(51))

    def __repr__(self):
        return '<User %r> from <%r>' % (self.nickname, self.city)