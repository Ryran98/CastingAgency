# Casting Agency App

## Introduction
This project serves as the Capstone project to display of all the elements learned across the Udacity Full Stack Nanodegree Program.

The aim is to demonstrate skills learned from each module which can be summarised as follows:

- Creating models for a postgres SQL Database and connecting to it using SQL Alchemy
- Build an effective RESTful API in Python using the Flask framework which demonstrates a variety of CRUD actions by connecting to the above mentioned psql database
- Set up postive and negative unit tests for each endpoint to ensure desired behaviour
- Create documentation around the project and each endpoint which will allow any developer with sufficient knowledge in the tech stack to pick the project up, understand it, deploy it locally and make changes to it
- Use Third-Party Authentication (in this case Auth0) to allow for RBAC (role-based access control)
- Deploy the API to Heroku where the live endpoints can be tested

___

## Setup Instructions

### Initial Setup & Installing dependencies

To begin you will need to install the project dependencies. You can do this using pip by navigating to the base `/CastingAgency` directory and running:
```bash
pip install -r requirements.txt
```

You will also need to have a local instance of a Postgres SQL Database Running. You can find the appropriate Postgres SQL installer according to your Operating System [here](https://www.postgresql.org/download/).

Once Postgres SQL is up and running properly, you will need to run the following command to create the new Casting Agency Database:

```bash
CREATEDB casting_agency
```

### Local deployment

With the initial setup completed, you are ready to deploy the API locally. To do so, you will need to follow the steps listed below:

- Migrate all database changes from the model to your local instance of Postgres SQL:

```bash
py manage.py db upgrade
```

- Export the Environment Variables required for the project to run:
```bash
. setup.sh
```

- Then finally to run the API locally:
```bash
py app.py
```

### Testing

There are also Unit Tests that have been created to test each endpoint defined in this project. To run the tests, execute the following commands:

```bash
DROPDB casting_agency_test
CREATEDB casting_agency_test
py test_app.py
```

___

## API Endpoints

### Base URL

This app is currently being hosted live on Heroku at the following URL:

BASE URL: https://rwcastingagency.herokuapp.com

### Authorization

This project uses [Auth0](https://auth0.com/) as it's Third-Party Authentication Service.

To make a successful request to any of the API endpoints (either locally or via the live URL), you will need to pass in an Authorization Header containing a Bearer Token.

You can obtain a Bearer Token (valid for 24 hours) by navigating to the following URL and logging in as one of the test users given in the `Roles & Permissions` section below:

https://rw1.eu.auth0.com/authorize?audience=https://rwcastingagency.herokuapp.com/&response_type=token&client_id=JYjflxhKatnzIIdIMZssmfbS5PzhbMBj&redirect_uri=https://rwcastingagency.herokuapp.com/login-results

Upon successful login, you will be redirected to a new URL where you can obtain the Bearer Token from the `access_token` parameter of the URL.

#### Roles & Permissions

There are 3 roles which have been set up in Auth0 to implement RBAC. You can find each role with their related permissions and test user credentials listed below:

1. **Casting Assistant**

    *Credentials:*
    ```
    Email address: castingassistant@rw-udacity.co.uk
    Password: CastingAssistant1
    ```

    *Permissions:*
    - get:actors
    - get:movies

2. **Casting Director**

    *Credentials:*
    ```
    Email address: castingdirector@rw-udacity.co.uk
    Password: CastingDirector1
    ```

    *Permissions:* (All permissions that Casting Assistant has in addition to below)
    - post:actors
    - post:movie_roles
    - update:actors
    - update:movies
    - delete:actors

3. **Executive Producer**

    *Credentials:*
    ```
    Email address: executiveproducer@rw-udacity.co.uk
    Password: ExecutiveProducer1
    ```

    *Permissions:* (All permissions that Casting Director has in addition to below)
    - post:movies
    - delete:movies

### Error Handling

Any errors that occur in the backend are returned as JSON objects in the following example format:
```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```

The API will return the following error types:
- 400: Bad Request
- 401: Invalid Header
- 403: Unauthorized
- 404: Resource Not Found
- 405: Method Not Allowed
- 422: Not Processable

### Endpoints

Please find below a list of all endpoints that are currently available from this API. There is a short description, an example request and an example response that you can expect for each one:

*Please note that any Authorization Tokens have been removed from the examples given which will be required to make a successful request*

#### GET /actors
- Returns a list of all actors, including basic information and each movie that they have a role in
- Example: `curl https://rwcastingagency.herokuapp.com/actors`
```
{
    "actors": [
        {
            "age": 44,
            "gender": "Male",
            "id": 1,
            "movies": [
                {
                    "id": 1,
                    "release_date": "10-02-2016",
                    "title": "Deadpool"
                }
            ],
            "name": "Ryan Reynolds"
        }
    ],
    "success": true
}
```

#### GET /movies
- Returns a list of all movies, including basic information and each actor that has a role
- Example: `curl https://rwcastingagency.herokuapp.com/movies`
```
{
    "movies": [
        {
            "actors": [
                {
                    "id": 1,
                    "name": "Ryan Reynolds"
                }
            ],
            "id": 1,
            "release_date": "10-02-2016",
            "title": "Deadpool"
        }
    ],
    "success": true
}
```

#### POST /actors
- Creates a new actor using the name, age and gender passed in to the request body as JSON.
- Returns the ID of the new actor
- Example: `curl -X POST https://rwcastingagency.herokuapp.com/actors -H "Content-Type: application/json" -d '{"name":"Scarlett Johansson", "age": 36, "gender": "Female"}'`
```
{
    "id": 2,
    "success": true
}
```

#### POST /movies
- Creates a new movie using the title and release date passed in to the request body as JSON.
- Returns the ID of the new movie
- Example: `curl -X POST https://rwcastingagency.herokuapp.com/movies -H "Content-Type: application/json" -d '{"title":"Black Widow", "release_date": "2021-07-09"}'`
```
{
    "id": 2,
    "success": true
}
```

#### DELETE /actors/{actor_id}
- Deletes the actor for the given actor id if it exists
- Returns the id of the actor that has been deleted
- Example: `curl -X DELETE https://rwcastingagency.herokuapp.com/actors/2`
```
{
    "id": 2,
    "success": true
}
```

#### DELETE /movies/{movie_id}
- Deletes the movie for the given movie id if it exists
- Returns the id of the movie that has been deleted
- Example: `curl -X DELETE https://rwcastingagency.herokuapp.com/movies/2`
```
{
    "id": 2,
    "success": true
}
```

#### PATCH /actors/{actor_id}
- Updates the name, age and gender values of the actor for the given actor id for any of the pre-mentioned properties that are passed in to the request body as JSON
- Returns the full JSON of the updated actor
- Example: `curl -X PATCH https://rwcastingagency.herokuapp.com/actors/2 -H "Content-Type: application/json" -d {"age": 37}`
```
{
    "actor": {
        "age": 37,
        "gender": "Female",
        "id": 2,
        "movies": [],
        "name": "Scarlett Johansson"
    },
    "success": true
}
```

#### PATCH /movies/{movie_id}
- Updates the title and release date of the movie for the given movie id for any of the pre-mentioned properties that are passed in to the request body as JSON
- Returns the full JSON for the updated movie
- Example: `curl -X PATCH https://rwcastingagency.herokuapp.com/movies/2 -H "Content-Type: application/json" -d {"release_date": "2021-07-10"}`
```
{
    "movie": {
        "actors": [],
        "id": 2,
        "release_date": "10-07-2021",
        "title": "Black Widow"
    },
    "success": true
}
```

#### POST /movieroles
- Creates a new movie role for the specified actor and movie via their id's
- Returns the ID of the new movie role
- Example: `curl -X POST https://rwcastingagency.herokuapp.com/movieroles -H "Content-Type: application/json" -d {"actor_id": 2, "movie_id": 2}`
```
{
    "id": 2,
    "success": true
}
```