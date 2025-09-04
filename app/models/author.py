from app.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
 
author_genre = db.Table('author_genre',
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True)
)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False, nullable=False)
    songs = relationship("Song", back_populates="author")
    genres = relationship('Genre', secondary=author_genre, backref=db.backref('authors'))


    def  to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'songs': self.songs,
            'genres': self.genres
        }