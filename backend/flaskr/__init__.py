import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from pprint import PrettyPrinter
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  pp = PrettyPrinter()
  pprint = pp.pprint
  
  '''
  @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app, resources={r"/*": {"origins": "*"}})

  '''
  @DONE: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

  '''
  @DONE: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories")
  def retrieve_categories():
    categories = Category.query.all()

    if len(categories) == 0:
      abort(404)

    formatted_categories = [category.format() for category in categories]

    return jsonify({
      "categories": formatted_categories
    })

  '''
  @DONE: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def retrieve_questions():
    search_term = request.args.get('search')

    filtered = Question.query
    if search_term is not None:
      filtered = Question.query.filter(Question.question.ilike('%{}%'.format(search_term)))
      print('filtered!')

    page = request.args.get('page')
    print('page:', page)

    selection = filtered.order_by(Question.id).all()
    current_questions = paginate_questions(request, selection)

    if len(current_questions) == 0:
      return abort(404)

    total_questions = len(selection)
    current_category = Category.query.first().format()   # todo: change this

    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]

    output = {
      'success': True,
      'questions': current_questions,
      'total_questions': total_questions,
      'categories': formatted_categories,
      'current_category': current_category
    }

    return jsonify(output)

  '''
  @DONE: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.get(question_id)

    if question is None:
      abort(404)

    try:
      question.delete()

      return jsonify({
        "success": True,
        "status_code": 200,
        "deleted": question.id
      })
    except:
      abort(400)
  '''
  @DONE: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    # todo: sanitize input and check if None
    question_title = body.get('question')
    answer = body.get('answer')
    difficulty = body.get('difficulty')
    category = body.get('category')

    try:
      question = Question(question=question_title, answer=answer, difficulty=difficulty, category=category)
      question.insert()

      return jsonify({
        "success": True,
        "status_code": 200,
        "created": question.id
      })
    except:
      abort(400)

  '''
  @DONE: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # Included in the retrieve_questions ('/questions') route above as a request paramater

  '''
  @DONE: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions')
  def retrieve_questions_by_category(category_id):
    category = Category.query.get(category_id)

    if category is None:
      abort(404)

    selection = Question.query.filter(Question.category == category.id).all()
    current_questions = paginate_questions(request, selection)
    total_questions = len(selection)

    return jsonify({
      "questions": current_questions,
      "total_questions": total_questions,
      "current_category": category.format()
    })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    body = request.get_json()
    
    quiz_category_id = body.get('quiz_category')['id']
    previous_questions = body.get('previous_questions')

    # filter by category
    category_questions = Question.query
    if quiz_category_id != 0:
      category_questions = Question.query.filter(Question.category == quiz_category_id)

    # filter by previous questions
    for prev_q in previous_questions:
      category_questions = category_questions.filter(Question.id != prev_q)

    questions = category_questions.all()

    if len(questions) == 0:
      return jsonify({})

    random_num = random.randrange(len(questions))
    current_question = questions[random_num]

    return jsonify({
      "question": current_question.format()
    })
  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    