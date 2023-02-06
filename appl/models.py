from flask_sqlalchemy import SQLAlchemy

from appl import db


class Saver:
    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model, Saver):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(120), unique = True)
    city = db.Column(db.String(51), db.ForeignKey('location.city'))
    age = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r> from <%r>' % (self.nickname, self.city)


class Location(db.Model, Saver):
    city = db.Column(db.String(60),  primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

    def __repr__(self):
        return '<Location %r - latitude %r and longitude %r>' % (self.city, self.latitude, self.longitude)
