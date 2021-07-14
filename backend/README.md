# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup

With Postgres running, restore a database using the trivia.psql file provided. First create a database called trivia then from the backend folder in terminal run:

```bash
createdb trivia
psql trivia < trivia.psql
```

Please make sure to set the username and password for your database in your environmental variables as follows:

```bash
export DB_USER=YourUsernameHere
export DB_PSWD=YourPasswordHere
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

## API Document

Following is the API document showing the available endpoints and their expected behavior:

```

Endpoints
GET '/categories'
GET '/questions'
GET '/categories/$id/questions'
POST '/questions'
POST '/questions/search'
DELETE '/questions/$id'
POST '/quizzes'


GET '/categories'
- Fetches a list of all categories available.
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a a list of category objects that have id and type properties. 
{
  "categories": [
    {
      "id": 1,
      "type": "Science"
    },
    {
      "id": 2,
      "type": "Art"
    },
    (etc...)
}


GET '/questions?page=<num>'
- Fetches a list of questions paginated by 10 questions for each page.
- Request Arguments: Optional to include a page number in the request parameter.
- Returns: An object with the following keys:
    - categories: containing a list of all categories as objects with id and type properties.
    - current_category: containing id and type proprties of the currently selected category.
    - questions: a list of questions paginated by 10 questions depending on page number in arguments,
                inwhich each question object has the properties:
                  - id: id of the question.
                  - question: question title.
                  - answer: answer to the question.
                  - difficulty: a numerical representation of the difficulty of the question, should be between 1 and 5.
                  - category: the id of the cateogry the question belongs to.
    - total_questions: number of total questions available.
{
    "categories": [
        {
            "id": 1,
            "type": "Science"
        },
        (etc...)
    ],
    "current_category": {
        "id": 1,
        "type": "Science"
    },
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        (etc...)
    ],
    "total_questions": 24
}


GET '/category/<category_id>/questions?page=<num>'
- Fetches a list of questions that belong to the <category_id> given, paginated by 10 questions in each page by default.
- Request Argument:
        - category_id: required in the endpoint url.
        - page: optional to include a page number in the request parameter.
- Returns: An object with the following keys:
    - current_category: containing id and type proprties of the currently selected category.
    - questions: a list of questions that belong to the category, paginated by 10 questions depending on page number in arguments.
    - total_questions: number of total questions that belong to the category.
{
    "current_category": {
        "id": 1,
        "type": "Science"
    },
    "questions": [
        {
            "id": 20,
            "question": "What is the heaviest organ in the human body?",
            "answer": "The Liver",
            "difficulty": 4,
            "category": 1
        },
        (etc...)
    ]
    "total_questions": 8
}


POST '/questions/search?page=<num>'
- Searches for the search term provided then returns the list of questions that match it, paginated by 10 questions for each page.
- Request Arguments: JSON request message is required with a searchTerm key for what to search for, as shown below:
    {
        "searchTerm": "movie"
    }
    - Optional to include a page number in the request parameter.
- Returns: An object with the following keys:
    - current_category: containing id and type proprties of the currently selected category.
    - questions: a list of questions matching the search term provided, paginated by 10 questions depending on page number in arguments.
    - total_questions: number of total questions that match the search term.
{
    "current_category": {
        "id": 1,
        "type": "Science"
    },
    "questions": [
        {
            "answer": "Apollo 13",
            "category": 5,
            "difficulty": 4,
            "id": 2,
            "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        (etc...)
    ],
    "total_questions": 1
}


POST '/questions'
- Creates a new question based on the information provided in the request message.
- Request Arguments: JSON request message is required with the following properties:
    - question: question title.
    - answer: answer to the question.
    - difficulty: a numerical representation of the difficulty of the question, should be between 1 and 5.
    - category: the id of the cateogry the question belongs to.
    Example as follows:
    {
        "question": "What is love?",
        "answer": "Baby don't hurt me",
        "difficulty": 5,
        "category": 1
    }
- Returns: The id of the question that has been created.
{
    "created": 25
}


DELETE '/questions/<question_id>'
- Deletes the question based on the <question_id> provided.
- Request Arguments: Requires question id to be provided in the endpoint url.
- Returns: The id  of the question that had been deleted.
{
    "deleted": 2
}


POST '/quizzes'
- Route for playing the trivia quiz.
- Request Argument: JSON request message is required with the following properties: 
    - quiz category: the category object of the category that is being played in the quiz, the object containin the id and type for the category.
    - previous questions: list of previous questions that have been played in the quiz for the category.
    Example as follows:
    {
        'quiz_category': {
            "id": 1,
            "type": "Science"
        }
        "previous_questions": [
          {
            "question": "What is love?",
            "answer": "Baby don't hurt me",
            "difficulty": 5,
            "category": 1
          },
          (etc...)
        ]
    }
- Returns: The next question in the category as an object containing the properties id, question, answer, difficulty, and category.
{
    "id": 20,
    "question": "What is the heaviest organ in the human body?",
    "answer": "The Liver",
    "difficulty": 4,
    "category": 1
}




Errors Handled by the API:


Error 400 - Bad Request
For when a request is sent with invalid request arguments.
Returns JSON object with the following properties:
{
  'success': False,
  'error': 400,
  'message': 'Bad Request'
}


Error 404 - Not Found
For when a resource requested is not found by the API.
Returns JSON object with the following properties:
{
  'success': False,
  'error': 404,
  'message': 'Not Found'
}


Error 405 - Method Not Allowed
For when a method used on an endpoint is not available in the API.
Returns JSON object with the following properties:
{
  'success': False,
  'error': 405,
  'message': 'Method Not Allowed'
}


Error 422 - Unprocessable Entity
For when a request is posted but with some missing data.
Returns JSON object with the following properties:
{
  'success': False,
  'error': 422,
  'message': 'Unprocessable Entity'
}


Error 500 - Internal Server Error
For when the API encounters a server error.
Returns JSON object with the following properties:
{
  'success': False,
  'error': 500,
  'message': 'Internal Server Error'
}


```


## Testing

To run the tests, run:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```