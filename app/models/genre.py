from app.extensions import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Genre(db.Model):

    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=False)
    songs = relationship("Song", back_populates="genre")

    def  to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'songs': self.songs
        }
