# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```


# API Documentation

 This is the list of all the endpoints and methods you can use in this API.In it, there is also a list of sample requests and sample responses.The expected erros are also shown.

 ## Base URL
 This API can only be accessed when the flask app is run locally. The base URL for this API is:
 `http://127.0.0.1:5000`
 The endpoints which exist include `/categories`, `/questions` and `/quizzes`

 ## Resources Documentation

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.
- Sample: `curl GET http://127.0.0.1:5000/categories`

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions'`

- Fetches a list containing dictionaries of questions in which the keys are answer, category, difficulty, question and id and the values are the corresponding strings and integers of each question.
- Sample: `curl GET 'http://127.0.0.1:5000/questions?page=1'`
- Returns:
```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "currentCategory": "",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        ...
    ],
    "totalQuestions": 27
}
```
### Errors
- When the user fetches a page which has no questions, a `404` error will be thrown.
- Sample: `curl GET http://127.0.0.1:5000/questions?page=25644`
- Returns: 
```json
{
    "error":404,
    "message":"Resource not found",
    "success": False
}
```


`DELETE '/questions/{question_id}'`
- Gets a question with the `question_id` id and deletes it from the database.
- Returns: Success value of the operation which is a Boolean value.
- Sample: `curl DELETE http://127.0.0.1:5000/questions/15`


```json
{
  "success": True
}
```
### Errors
- When an invalid question id is added to the parameters, a `404` error will be thrown.
- Sample: `curl DELETE http://127.0.0.1:5000/questions/15`
- Returns: 
```json
{
    "error":404,
    "message":"Resource not found",
    "success":False
}
```

`POST '/questions'`
- Sends a post request in order to search for particular questions.
- Returns: An object with three keys, `questions`, `success` and `totalQuestions`
- Sample: `curl -X POST -H http://localhost:5000/questions "Content-Type: application/json -d '{"searchTerm":"score"}'`

```json
{
    "questions": [
        {
            "answer": "20",
            "category": 2,
            "difficulty": 3,
            "id": 24,
            "question": "How many items make a score?"
        }
    ],
    "success": true,
    "total_questions": 1
}
```
### Errors
- An error is thrown when an invalide json request is sent.
- Sample: `curl -X POST -H http://localhost:5000/questions "Content-Type: application/json -d '{"searchTerm":"score"}'`
- Returns:
```json
{
    "error":404,
    "message":"Resource not found",
    "success":False
}
```

`POST '/questions'`
- Sends a post request in order to post a new question.
- Returns: An object containing three keys, `totalQuestions`, `questions` and `currentCategory`
- Sample: `curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Yes/No","answer":"No","difficulty":"1","category":"5"}'`
```json
{
    "currentCategory": "none",
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        ...
    ],
    "totalQuestions": 27
}
```
### Error
- If the user sends a request with an invalid json, a `404` error will be thrown.
- Sample: `curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Yes/No","answer":"No","difficulty":"1","category":"5"}'`
- Returns:
```json
{
    "error":404,
    "message":"Resource not found",
    "success":False
}
```

`GET '/categories/<int:category_id>/questions'`
- Sends a post request in order to get questions from a given category.
- Returns: An object with three keys, `currentCategory`, `questions` and `totalQuestions`
- Sample: `curl GET http://localhost:5000/categories/2/questions`
```json
{
    "currentCategory": 2,
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },
        {
            "answer": "Mona Lisa",
            "category": 2,
            "difficulty": 3,
            "id": 17,
            "question": "La Giaconda is better known as what?"
        },
        {
            "answer": "One",
            "category": 2,
            "difficulty": 4,
            "id": 18,
            "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        ...
    ],
    "totalQuestions": 27
}
```
### Errors
- When a user asks for a category which does not exist, it will throw a `404` error.
- Sample: `curl GET http://localhost:5000/categories/88/questions`
- Response: 
```json
{
    "error":404,
    "message":"Resource not found",
    "success": False
}
```

`POST '/quizzes'`
- Sends a post request in order to get the next question to play in the quizz.
- Returns: An object with one key, `question` which contains the question to be played.
- Sample: `curl http://localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"quiz_category":{"id":6,"type":"Science"},"previous_questions":[]}'`.
```json
{
    "question": {
        "answer": "Julius Yego",
        "category": 6,
        "difficulty": 2,
        "id": 28,
        "question": "Who holds the African record for the javelin throw?"
    }
}
```
### Errors
Trying to post a question without a valid json body will returna `404` error.
Sample: `curl http://localhost:5000/quizzes`
Response: 
```json
{
    "error":400,
    "message":"Unprocessable",
    "success": False
}
```