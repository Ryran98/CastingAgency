import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Actor, Movie, MovieRole, setup_db
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response

  @app.route('/actors', methods=['GET'])
  def get_actors():
    actors = Actor.query.all()

    if not actors or len(actors) < 1:
      abort(404)
    
    try:
      actors_formatted = []
      for actor in actors:
        actors_formatted.append(actor.format())

      return jsonify({
        'success': True,
        'actors': actors_formatted
      }), 200

    except:
      abort(422)

  @app.route('/movies', methods=['GET'])
  def get_movies():
    movies = Movie.query.all()

    if not movies or len(movies) < 1:
      abort(404)
    
    try:
      movies_formatted = []
      for movie in movies:
        movies_formatted.append(movie.format())
      
      return jsonify({
        'success': True,
        'movies': movies_formatted
      }), 200

    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  def delete_actor(actor_id):
    actor = Actor.query.get(actor_id)

    if actor is None:
      abort(404)

    try:
      actor.delete()

      return jsonify({
        'success': True,
        'id': actor_id
      }), 200

    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)

    if movie is None:
      abort(404)
    
    try:
      movie.delete()

      return jsonify({
        'success': True,
        'id': movie_id
      }), 200

    except:
      abort(422)

  @app.route('/actors', methods=['POST'])
  def new_actor():
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    if not name:
      return jsonify({
        'success': False,
        "error": 422,
        'message': 'Missing name'
      })
    if not age:
      return jsonify({
        'success': False,
        "error": 422,
        'message': 'Missing age'
      })
    if not gender:
      return jsonify({
        'success': False,
        "error": 422,
        'message': 'Missing gender'
      })
      
    try:
      actor = Actor(name=name, age=age, gender=gender)
      actor.insert()

      return jsonify({
        'success': True,
        'id': actor.id
      }), 200

    except:
      abort(422)

  @app.route('/movies', methods=['POST'])
  def new_movie():
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    if not title:
      return jsonify({
        'success': False,
        "error": 422,
        'message': 'Missing title'
      })
    if not release_date:
      return jsonify({
        'success': False,
        "error": 422,
        'message': 'Missing release date'
      })

    try:
      movie = Movie(title=title, release_date=release_date)
      movie.insert()

      return jsonify({
        'success': True,
        'id': movie.id
      }), 200

    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  def update_actor(actor_id):
    actor = Actor.query.get(actor_id)

    if not actor:
      abort(404)

    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    try:
      if name is not None:
        actor.name = name
      if age is not None:
        actor.age = age
      if gender is not None:
        actor.gender = gender

      actor.update()

      return jsonify({
        'success': True,
        'actor': actor.format()
      }), 200

    except:
      abort(422)

  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  def update_movie(movie_id):
    movie = Movie.query.get(movie_id)

    if not movie:
      abort(404)

    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    try:
      if title is not None:
        movie.title = title
      if release_date is not None:
        movie.release_date = release_date

      movie.update()

      return jsonify({
        'success': True,
        'movie': movie.format()
      }), 200
    
    except:
      abort(422)

  @app.route('/movieroles', methods=['POST'])
  def new_movie_role():
    body = request.get_json()
    actor_id = body.get('actor_id', None)
    movie_id = body.get('movie_id', None)

    actor = Actor.query.get(actor_id)
    movie = Movie.query.get(movie_id)

    if not actor:
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'No actor could be found for id ' + actor_id
      })
    if not movie:
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'No movie could be found for id ' + movie_id
      })

    try:
      movie_role = MovieRole(actor=actor, movie=movie)
      movie_role.insert()

      return jsonify({
        'success': True,
        'id': movie_role.id
      })

    except:
      abort(422)

  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'resource not found'
    }), 404

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'unprocessable'
    }), 422

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)