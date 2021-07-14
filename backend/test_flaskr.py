import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.db_username = os.environ['DB_USER']
        self.db_password = os.environ['DB_PSWD']
        self.database_path = "postgres://{}:{}@{}/{}".format(self.db_username, self.db_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is love?',
            'answer': "Baby don't hurt me",
            'difficulty': 5,
            'category': 1
        }

        self.new_question_empty_answer = {
            'question': 'What is the meaning of life?',
            'answer': '',
            'difficulty': 5,
            'category': 2
        }

        self.new_question_string_in_integer_values = {
            'question': 'Which animals are the best pets?',
            'answer': 'Hamsters',
            'difficulty': 'Cats',
            'category': 'Dogs'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after each test"""
        pass

    """
    DONE:
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
      res = self.client().get('/categories')
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(len(data['categories']))


    def test_get_paginated_questions(self):
      res = self.client().get('/questions')
      data = json.loads(res.data.decode('utf-8'))

      first_page_questions = data['questions']
      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(len(data['questions']))
      self.assertTrue(data['total_questions'])
      self.assertTrue(data['categories'])
      self.assertTrue(data['current_category'])

      total_questions = data['total_questions']

      # skip below test if number of all questions is exactly 10, as it will fail
      if total_questions != 10:
        res2 = self.client().get('/questions?page=2')
        data2 = json.loads(res2.data.decode('utf-8'))
        second_page_questions = data2['questions']

        first_page_first_question = first_page_questions[0]['question']
        second_page_first_question = second_page_questions[0]['question']

        self.assertNotEqual(first_page_first_question, second_page_first_question)
      

    def test_404_sent_requesting_beyond_valid_page(self):
      res = self.client().get('/questions?page=1000')
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 404)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Not Found')


    def test_delete_question(self):
      question_id = 2
      res = self.client().delete('/questions/' + str(question_id))
      data = json.loads(res.data.decode('utf-8'))

      question = Question.query.get(question_id)

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertEqual(data['deleted'], question_id)
      self.assertEqual(question, None)

      # Make sure the question is deleted; can't delete same question twice
      res2 = self.client().delete('/questions/' + str(question_id))
      data2 = json.loads(res2.data.decode('utf-8'))
      
      self.assertEqual(res2.status_code, 404)
      self.assertEqual(data2['success'], False)
      self.assertEqual(data2['message'], 'Not Found')

    
    def test_404_question_to_delete_not_found(self):
      question_id = 10000
      res = self.client().delete('/questions/' + str(question_id))
      data = json.loads(res.data.decode('utf-8'))

      question = Question.query.get(question_id)

      self.assertEqual(question, None)
      self.assertEqual(res.status_code, 404)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Not Found')


    def test_create_question(self):
      res = self.client().post('/questions', json=self.new_question)
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['created'])
      # Making sure question is created by searching for it in the test below

    
    def test_search_for_questions(self):
      res = self.client().post('/questions/search', json={'searchTerm': self.new_question['question'] })
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(len(data['questions']))
      self.assertTrue(data['total_questions'])
      self.assertTrue(data['current_category'])


    def test_405_question_creation_not_allowed(self):
      # Can't post to route /questions/$id
      res = self.client().post('/questions/1000', json=self.new_question)
      data = json.loads(res.data.decode('utf-8'))
      
      self.assertEqual(res.status_code, 405)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Method Not Allowed')


    def test_422_question_creation_empty_values(self):
      # Can't create question with empty answer
      res = self.client().post('/questions', json=self.new_question_empty_answer)
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 422)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Unprocessable Entity')

    
    def test_400_question_creation_string_in_integer_values(self):
      # Can't create question with string in integer values (difficulty & category id)
      res = self.client().post('/questions', json=self.new_question_string_in_integer_values)
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 400)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Bad Request')


    def test_get_questions_by_category(self):
      res = self.client().get('/categories/1/questions')
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(len(data['questions']))
      self.assertTrue(data['total_questions'])
      self.assertTrue(data['current_category'])


    def test_404_get_questions_by_unavailable_category(self):
      res = self.client().get('/categories/1000/questions')
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 404)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Not Found')
    

    def test_404_unavailable_random_endpoint(self):
      res = self.client().get('/this/is/a/random/endpoint')
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 404)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Not Found')


    def test_play_trivia_quiz(self):
      quiz_data = {
        'previous_questions': [], 
        'quiz_category': {
          'id': 1,
          'type': 'Science'
        }
      }
      res = self.client().post('/quizzes', json=quiz_data)
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['question'])
    

    def test_404_play_quiz_with_unavailable_cateogry(self):
      quiz_data = {
        'previous_questions': [], 
        'quiz_category': {
          'id': 1000,
          'type': 'Unavailable Category'
        }
      }
      res = self.client().post('/quizzes', json=quiz_data)
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 404)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Not Found')
    

    def test_400_play_quiz_with_string_in_place_of_list(self):
      quiz_data = {
        'previous_questions': 'not a list', 
        'quiz_category': {
          'id': 1,
          'type': 'Science'
        }
      }
      res = self.client().post('/quizzes', json=quiz_data)
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 400)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Bad Request')


    def test_405_method_get_not_allowed_for_quizzes_endpoint(self):
      res = self.client().get('/quizzes')
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 405)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Method Not Allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()