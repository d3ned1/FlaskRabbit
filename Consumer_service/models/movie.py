import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint

db = SQLAlchemy()


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=False, nullable=False)
    rate = db.Column(db.Float, unique=False, nullable=False)
    length = db.Column(db.Integer, unique=False, nullable=False)
    year = db.Column(db.Integer, unique=False, nullable=False)
    __table_args__ = (
        CheckConstraint(rate >= 1, name='rate_greater_1'),
        CheckConstraint(year >= 1888, name='film_year_greater_1888'),
        {})

    def __init__(self, title, year, length, rate):
        self.title = title
        self.year = year
        self.length = length
        self.rate = rate

    def __repr__(self):
        return '<Movie %s>' % self.title

    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'rate': self.rate,
            'length': self.length,
            'year': self.year,
        }
