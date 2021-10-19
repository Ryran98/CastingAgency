import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Actor, Movie, MovieRole

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)

        actor = Actor(name='Ryan Reynolds', age=44, gender='Male')
        actor.insert()
        movie = Movie(title='Deadpool', release_date='2016-02-10')
        movie.insert()

    def tearDown(self):
        pass
    
    # Get Actors Tests
    def test_404_get_actors(self):
        response = self.client().get('/actors?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actors(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # Get Movies Tests
    def test_404_get_movies(self):
        response = self.client().get('/movies?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # Delete Actor Tests
    def test_404_delete_actor(self):
        response = self.client().delete('/actors/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        response = self.client().delete('/actors/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    # Delete Movie Tests
    def test_404_delete_movie(self):
        response = self.client().delete('/movies/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        response = self.client().delete('/movies/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    # New Actor Tests
    def test_422_new_actor(self):
        response = self.client().post('/actors', json={
            'name': 'Scarlett Johansson',
            'gender': 'Female'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Missing age')

    def test_new_actor(self):
        response = self.client().post('/actors', json={
            'name': 'Scarlett Johansson',
            'age': 36,
            'gender': 'Female'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    # New Movie Tests
    def test_422_new_movie(self):
        response = self.client().post('/movies', json={
            'title': 'Black Widow'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Missing release date')

    def test_new_movie(self):
        response = self.client().post('/movies', json={
            'title': 'Black Widow',
            'release_date': '2021-07-01'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    # Update Actor Tests
    def test_404_update_actor(self):
        response = self.client().patch('actors/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_actor(self):
        response = self.client().patch('actors/1', json={
            'age': 45
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['age'], 45)

    # Update Movie Tests
    def test_404_update_movie(self):
        response = self.client().patch('movies/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_movie(self):
        response = self.client().patch('movies/1', json={
            'release_date': '2016-02-11'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['release_date'], '11-02-106')

    # New Movie Role Tests
    def test_422_new_movie_role(self):
        response = self.client().post('movieroles', json={
            'actor_id': 1000,
            'movie_id': 1
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No actor could be found for id 1000')

    def test_new_movie_role(self):
        response = self.client().post('movieroles', json={
            'actor_id': 1,
            'movie_id': 1
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

if __name__ == "__main__":
    unittest.main()