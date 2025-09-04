from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from app.extensions import db

from flask import request, jsonify
# from .models import *
# from ariadne import load_schema_from_path, make_executable_schema, \
#     graphql_sync, snake_case_fallback_resolvers, ObjectType
# from ariadne.constants import PLAYGROUND_HTML
# from app.api_resolvers.resolvers import *
from config import Config


def create_app(*args, **kwargs):
    # print(args)
    # print(kwargs)
    app = Flask(__name__)
    app.config.from_object(Config)

    # db.init_app(app)
    
    # with app.app_context():
    #     db.drop_all()
    #     db.create_all()

        




    #     # Create two genres
    #     genre1 = genre.Genre(name='dimeloFunk')
    #     genre2 = genre.Genre(name='dimeloSalsa')


    #     db.session.add(genre1)
    #     print('dimeloare ylou')
    #     db.session.add(genre2)

    #     author1 = author.Author(name='yopapijoe', genres=[genre1, genre2])
    #     author2 = author.Author(name='yopapijoe2', genres=[genre2])

    #     db.session.add(author1)
    #     db.session.add(author2)
    #     db.session.commit()
    #     print('dimeloare ylou222')

    #     song1 = song.Song(title='Vamonos pal Funk', author=author1, genre=genre1)
    #     song2 = song.Song(title='Salsa pa los dimelos', author=author1, genre=genre2)
    #     song3 = song.Song(title='como volver a ser funky', author=author2, genre=genre2)
    #     song4 = song.Song(title='Dile a funkella', author=author2, genre=genre2)

    #     db.session.add(song1)
    #     db.session.add(song2)
    #     db.session.add(song3)
    #     db.session.add(song4)
    #     db.session.commit()

    # Initialize Flask extensions here

    # Register resolvers here
    
    # query = ObjectType("Query")
    # query.set_field("authors", resolve_authors)
    # query.set_field("author", resolve_author)
    
    # mutation = ObjectType("Mutation")
    # mutation.set_field("createAuthor", resolve_create_author)





    # schema = make_executable_schema(
    # type_defs, query, mutation, snake_case_fallback_resolvers
    # )



    # Register blueprints here

    # from app.api_resolvers import bp as api_resolvers_bp
    # # app.register_blueprint(api_resolvers_bp)
    # from app.IntervalClass import bp as intervalClass_bp
    # app.register_blueprint(intervalClass_bp)

    from app.Dashboard import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    # from app.NoteClass import bp as noteClass_bp
    # app.register_blueprint(noteClass_bp)
    # from app.HarmonyClass import bp as harmonyClass_bp
    # app.register_blueprint(harmonyClass_bp)
    # from app.Music21 import bp as music21_bp
    # app.register_blueprint(music21_bp)
    # from app.ScoreParserClass2 import bp as scoreParserClass2_bp
    # app.register_blueprint(scoreParserClass2_bp)



    from app.LiveVisualizationTool import bp as liveVisualizationTool_bp
    app.register_blueprint(liveVisualizationTool_bp, url_prefix='/live')


# ## routes

#     @app.route("/graphql", methods=["GET"])
#     def graphql_playground():
        

#         return PLAYGROUND_HTML, 200
        


#     @app.route("/graphql", methods=["POST"])
#     def graphql_server():
#         data = request.get_json()
     

#         print('schema')
#         print(schema)
#         print('request')
#         print(request)
#         print('data')
#         print(data)

#         try:
#             success, result = graphql_sync(
#                 schema,
#                 data,
#                 context_value=request,
#                 debug=True
#             )
#             print('success')
#             print(success)
#             print('result')
#             print(result)
#             status_code = 200 if success else 400
#             return jsonify(result), status_code
    
#         except Exception as e:
#             print(f"An error occurred: {e}")

            
#             return 'wahwah'
    

    return app

app = create_app()