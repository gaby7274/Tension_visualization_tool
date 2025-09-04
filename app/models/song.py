from app.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), index=False)
    author_id = db.Column(db.Integer, ForeignKey('author.id'))
    author = relationship("Author", back_populates="songs")
    genre_id = db.Column(db.Integer, ForeignKey('genre.id'))
    genre = relationship("Genre", back_populates="songs")
    key = db.Column(db.String(64), index=True)
    time_signature = db.Column(db.String(64), index=True)
    tempo = db.Column(db.Integer)
    midi_filepath = db.Column(db.String(64), index=False)
    
    def  to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'author_id': self.author_id,
            'key': self.key,
            'time_signature': self.time_signature,
            'tempo': self.tempo,
            'midi_filepath': self.midi_filepath
        }