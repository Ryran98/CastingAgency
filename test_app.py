import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import db, setup_db, Actor, Movie, MovieRole

CASTING_ASSISTANT_BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkN6S0gzanNrcEhDaGJtS0ZMRWNKWSJ9.eyJpc3MiOiJodHRwczovL3J3MS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE2ZTA2MDVlZDNhMjkwMDY4YjNmYjVkIiwiYXVkIjoiaHR0cHM6Ly9yd2Nhc3RpbmdhZ2VuY3kuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE2MzQ5MDI4ODEsImV4cCI6MTYzNDk4OTI4MSwiYXpwIjoiSllqZmx4aEthdG56SUlkSU1ac3NtZmJTNVB6aGJNQmoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.B0QW0PlUgy4EV-YATHJnyn6AiOL8fXNrOcnbPWWPa2mItuLfEqwaQCDlFk3M5uOiz8v5S4dGpx73R5hFubbImekfxeswDiRpsk0WmtdCIsYYeTCzGvGlVtaESun9LfRfCQ1eJVxgJltv-Up8-m-eOr9B2hVnQ0JsM-3o3LMAuvG5UR4m7i5o9ju0g92HKckS1gWZi8wPN5NDf-g90One0kLVUt3d4SDRqOS-YRUXvLXaJ-Jc6rwH8LUDWXBySLCBR6nhXZ0jB9_fQ3HDxNt_W5K-Da4WwD4rDYrjVNFTMbmeqlDKd9DyppLTDXhLiVxyHKBsT9S6jpXVRl9me5QB8w"
CASTING_DIRECTOR_BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkN6S0gzanNrcEhDaGJtS0ZMRWNKWSJ9.eyJpc3MiOiJodHRwczovL3J3MS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE2ZTA2Mzc1ZDNkOWQwMDcwZWRlNzEyIiwiYXVkIjoiaHR0cHM6Ly9yd2Nhc3RpbmdhZ2VuY3kuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE2MzQ5MDI5MzcsImV4cCI6MTYzNDk4OTMzNywiYXpwIjoiSllqZmx4aEthdG56SUlkSU1ac3NtZmJTNVB6aGJNQmoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZV9yb2xlcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.uYU9Fr3dE1k0EJ2RMlZgjAAJlM3zrv00xgTay8GxmXXssm45ChQLaC1RJSrv5GDR3QhE1vEPj76hpeMi2L5Fs8OeCEvS4itHe841Txqyr1ufes87_t2rsz9gh4T8CJCpUSzIxjbyJotskEI0Rra2L98A6XOiK1hZJkOcYIud1DPYtPteuh14k6Ga2cgmght_HHNtLSi0QLSjK7vXQfn1-Pmf9-1P34ncb2h1-tGtxmiEzCATBoiwkfugZ0An0hNdeYJ9tU_sdyzCvyFnDcYURh-fveLNbXqon0jrQZsS29d-SWaqN4DgyFZpZFFTq4p5j6sFvDJ1dcrVftCU_G01zw"
EXECUTIVE_PRODUCER_BEARER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkN6S0gzanNrcEhDaGJtS0ZMRWNKWSJ9.eyJpc3MiOiJodHRwczovL3J3MS5ldS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjE2ZTA2NWUyNWYyMDMwMDY4MDY2ZmQ4IiwiYXVkIjoiaHR0cHM6Ly9yd2Nhc3RpbmdhZ2VuY3kuaGVyb2t1YXBwLmNvbS8iLCJpYXQiOjE2MzQ5MDc3NTgsImV4cCI6MTYzNDk5NDE1OCwiYXpwIjoiSllqZmx4aEthdG56SUlkSU1ac3NtZmJTNVB6aGJNQmoiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVfcm9sZXMiLCJwb3N0Om1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIl19.pd7gTN7OhikPeuu7S05DeAvFV4qtsjCt1PDGMHOi-Gq2JHV3C96DlfTvcaIo4yM5S4L0fzyPSFPUvfvWBJSb9op9QoblSvGibh1U_f3Zk2pU9FVxfG9OF6LdmMvEqb2TD1NhHQohKeUwQRTsxFFAVOn8iMR_0LELPElkS1WuZqIZhN6TUQYK1L32o7YDtmLX23xIo2y7zjpDRTQMteDI-9FdOrXCZcWPtD3K843EI9QWFnAofF-K1FNhX78HvbKzHu20j2njViwLWrjXPp3gC8ur4RBy6_hAcnI5qxhhpCUZfLSP6tV4fNQhqdSEMzmhacCLp2nkr-4PcgVG2-aajA"

class CastingAgencyTestCase(unittest.TestCase):
    def setUp(self):
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path, True)

        self.casting_assistant_auth = {"Authorization": "Bearer " + CASTING_ASSISTANT_BEARER_TOKEN}
        self.casting_director_auth = {"Authorization": "Bearer " + CASTING_DIRECTOR_BEARER_TOKEN}
        self.exec_producer_auth = {"Authorization": "Bearer " + EXECUTIVE_PRODUCER_BEARER_TOKEN}

        actor = Actor(name='Ryan Reynolds', age=44, gender='Male')
        actor.insert()
        movie = Movie(title='Deadpool', release_date='2016-02-10')
        movie.insert()

    def tearDown(self):
        pass
    
    # Get Actors Tests
    def test_404_get_actors(self):
        response = self.client().get('/actors?page=1000', headers=self.casting_assistant_auth)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_actors(self):
        response = self.client().get('/actors', headers=self.casting_assistant_auth)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # Get Movies Tests
    def test_404_get_movies(self):
        response = self.client().get('/movies?page=1000', headers=self.casting_assistant_auth)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_movies(self):
        response = self.client().get('/movies', headers=self.casting_assistant_auth)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # Delete Actor Tests
    def test_404_delete_actor(self):
        response = self.client().delete('/actors/1000', headers=self.casting_director_auth)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_actor(self):
        response = self.client().delete('/actors/1', headers=self.casting_director_auth)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    # Delete Movie Tests
    def test_404_delete_movie(self):
        response = self.client().delete('/movies/1000', headers=self.exec_producer_auth)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_delete_movie(self):
        response = self.client().delete('/movies/1', headers=self.exec_producer_auth)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 1)

    # New Actor Tests
    def test_422_new_actor(self):
        response = self.client().post('/actors', headers=self.casting_director_auth, json={
            'name': 'Scarlett Johansson',
            'gender': 'Female'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Missing age')

    def test_new_actor(self):
        response = self.client().post('/actors', headers=self.casting_director_auth, json={
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
        response = self.client().post('/movies', headers=self.exec_producer_auth, json={
            'title': 'Black Widow'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Missing release date')

    def test_new_movie(self):
        response = self.client().post('/movies', headers=self.exec_producer_auth, json={
            'title': 'Black Widow',
            'release_date': '2021-07-01'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

    # Update Actor Tests
    def test_404_update_actor(self):
        response = self.client().patch('actors/1000', headers=self.casting_director_auth)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_actor(self):
        response = self.client().patch('actors/1', headers=self.casting_director_auth, json={
            'age': 45
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['age'], 45)

    # Update Movie Tests
    def test_404_update_movie(self):
        response = self.client().patch('movies/1000', headers=self.casting_director_auth)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_update_movie(self):
        response = self.client().patch('movies/1', headers=self.casting_director_auth, json={
            'release_date': '2016-02-11'
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['movie']['release_date'], '11-02-2016')

    # New Movie Role Tests
    def test_422_new_movie_role(self):
        response = self.client().post('movieroles', headers=self.exec_producer_auth, json={
            'actor_id': 1000,
            'movie_id': 1
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'No actor could be found for id 1000')

    def test_new_movie_role(self):
        response = self.client().post('movieroles', headers=self.exec_producer_auth, json={
            'actor_id': 1,
            'movie_id': 1
        })
        print(response)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])

if __name__ == "__main__":
    unittest.main()