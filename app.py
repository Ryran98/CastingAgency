import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import db, Actor, Movie, MovieRole, setup_db
from auth.auth import AuthError, requires_auth

ITEMS_PER_PAGE = 10

def paginate_items(request, items):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * ITEMS_PER_PAGE
  end = page * ITEMS_PER_PAGE

  formatted_items = [item.format() for item in items]

  return formatted_items[start:end]

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
  @requires_auth('get:actors')
  def get_actors(payload):
    actors = Actor.query.order_by(Actor.id).all()
    selected_actors = paginate_items(request, actors)

    if not selected_actors or len(selected_actors) < 1:
      abort(404)
    
    try:
      return jsonify({
        'success': True,
        'actors': selected_actors
      }), 200

    except:
      abort(422)

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies(payload):
    movies = Movie.query.order_by(Movie.id).all()
    selected_movies = paginate_items(request, movies)

    if not selected_movies or len(selected_movies) < 1:
      abort(404)
    
    try:
      return jsonify({
        'success': True,
        'movies': selected_movies
      }), 200

    except:
      abort(422)

  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(payload, actor_id):
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
  @requires_auth('delete:movies')
  def delete_movie(payload, movie_id):
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
  @requires_auth('post:actors')
  def new_actor(payload):
    body = request.get_json()
    name = body.get('name', None)
    age = body.get('age', None)
    gender = body.get('gender', None)

    if not name:
      return jsonify({
        'success': False,
        "error": 422,
        'message': 'Missing name'
      }), 422
    if not age:
      return jsonify({
        'success': False,
        "error": 422,
        'message': 'Missing age'
      }), 422
    if not gender:
      return jsonify({
        'success': False,
        "error": 422,
        'message': 'Missing gender'
      }), 422
      
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
  @requires_auth('post:movies')
  def new_movie(payload):
    body = request.get_json()
    title = body.get('title', None)
    release_date = body.get('release_date', None)

    if not title:
      return jsonify({
        'success': False,
        "error": 422,
        'message': 'Missing title'
      }), 422
    if not release_date:
      return jsonify({
        'success': False,
        "error": 422,
        'message': 'Missing release date'
      }), 422

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
  @requires_auth('update:actors')
  def update_actor(payload, actor_id):
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
  @requires_auth('update:movies')
  def update_movie(payload, movie_id):
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
  @requires_auth('post:movie_roles')
  def new_movie_role(payload):
    body = request.get_json()
    actor_id = body.get('actor_id', None)
    movie_id = body.get('movie_id', None)

    actor = Actor.query.get(actor_id)
    movie = Movie.query.get(movie_id)

    if not actor:
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'No actor could be found for id ' + str(actor_id)
      }), 422
    if not movie:
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'No movie could be found for id ' + str(movie_id)
      }), 422

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

  @app.errorhandler(AuthError)
  def auth_error(error):
    return jsonify({
      'success': False,
      'error': error.status_code,
      'message': error.error['description']
    }), error.status_code

  return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)