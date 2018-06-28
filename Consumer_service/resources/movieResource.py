from Consumer_service.models.movie import db, Movie


def create_movie(data):
    title = data.get('title')
    year = data.get('year')
    length = data.get('length')
    rate = data.get('rate')
    movie = Movie(title, year, length, rate)
    db.session.add(movie)
    db.session.commit()


def update_movie(id, data):
    movie = Movie.query.filter(Movie.id == id).one()
    movie.title = data.get('title')
    movie.year = data.get('year')
    movie.length = data.get('length')
    movie.rate = data.get('rate')
    db.session.add(movie)
    db.session.commit()


def delete_movie(id):
    movie = Movie.query.filter(Movie.id == id).one()
    db.session.delete(movie)
    db.session.commit()
