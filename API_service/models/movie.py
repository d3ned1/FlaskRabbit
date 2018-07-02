from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

ma = Marshmallow()
db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    rate = db.Column(db.Float, unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)
    year = db.Column(db.Date, unique=False, nullable=False)

    def __init__(self, title, year, length, rate):
        self.title = title
        self.year = year
        self.length = length
        self.rate = rate

    def __repr__(self):
        return '<Movie %s>' % self.title
