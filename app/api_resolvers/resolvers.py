from app.models import *
from app.extensions import db
from ariadne import convert_kwargs_to_snake_case


def resolve_authors(obj,info, limit=None, offset=None):
    print('resolve_authors is being called')
    try:

        all_authors = Author.query
        if limit:
            all_authors = all_authors.limit(limit)
        if offset:
            all_authors = all_authors.offset(offset)
        all_authors = all_authors.all()

        print('here')
        
        authors = [author.to_dict() for author in all_authors]
        payload = {
            'success': True,
            'data': authors
        }
        return authors
    except Exception as e:
        print('here')
        payload = {
            'success': False,
            'errors': [str(e)]
        }

        print(payload)
        return [str(e)]


@convert_kwargs_to_snake_case
def resolve_author(obj,info, author_id):
    print('resolve_author is being called')
    try:
        author = Author.query.get(author_id)
        payload = {
            'success': True,
            'data': author.to_dict()
        }
        return author.to_dict()
    except Exception as e:
        payload = {
            'success': False,
            'errors': [f"Author with id {author_id} not found"]
        }
        return [f"Author with id {author_id} not found"]

@convert_kwargs_to_snake_case
def resolve_create_author(obj,info, name,genre_ids):
    try:
        author = Author(name=name)
        for genre_id in genre_ids:
            genre = Genre.query.get(genre_id)
            author.genres.append(genre)
        db.session.add(author)
        db.session.commit()
        return author.to_dict()

    except Exception as e:
        error = ['couldnt do shit',str(e)]
        return error

    

    
