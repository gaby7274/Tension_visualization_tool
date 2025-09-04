import app
application = app.create_app()

with application.app_context():
    app.db.drop_all()
    app.db.create_all()




    # Create two genres
    genre1 = app.genre.Genre(name='dimeloFunk')
    genre2 = app.genre.Genre(name='dimeloSalsa')


    app.db.session.add(genre1)
    app.db.session.add(genre2)

    author1 = app.author.Author(name='yopapijoe', genres=[genre1, genre2])
    author2 = app.author.Author(name='yopapijoe2', genres=[genre2])

    app.db.session.add(author1)
    app.db.session.add(author2)

    song1 = app.song.Song(title='Vamonos pal Funk', author=author1, genre=genre1)
    song2 = app.song.Song(title='Salsa pa los dimelos', author=author1, genre=genre2)
    song3 = app.song.Song(title='como volver a ser funky', author=author2, genre=genre2)
    song4 = app.song.Song(title='Dile a funkella', author=author2, genre=genre2)

    app.db.session.add(song1)
    app.db.session.add(song2)
    app.db.session.add(song3)
    app.db.session.add(song4)
    app.db.session.commit()




