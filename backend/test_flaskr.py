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
            'question_title': 'What is love?',
            'answer': 'Baby don\'t hurt me',
            'difficulty': 5,
            'category': 1
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_paginated_questions(self):
      res = self.client().get('/questions')
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['total_questions'])
      self.assertTrue(len(data['questions']))
      self.assertTrue(data['categories'])
      self.assertTrue(data['current_category'])
      
    def test_404_sent_requesting_beyond_valid_page(self):
      res = self.client().get('/questions?page=1000')
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 404)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Not Found')

    def test_create_question(self):
      res = self.client().post('/questions', json=self.new_question)
      data = json.loads(res.data.decode('utf-8'))

      self.assertEqual(res.status_code, 200)
      self.assertEqual(data['success'], True)
      self.assertTrue(data['created'])
      #self.assertTrue(len(data['questions']))

    def test_405_if_question_creation_not_allowed(self):
      res = self.client().post('/questions/1000', json=self.new_question)
      data = json.loads(res.data.decode('utf-8'))
      
      self.assertEqual(res.status_code, 405)
      self.assertEqual(data['success'], False)
      self.assertEqual(data['message'], 'Method Not Allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()