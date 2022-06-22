import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from backend.models import DB_HOST, DB_NAME, DB_PASS, DB_USER

from flaskr import create_app
from models import setup_db, Question, Category

#environment variables
DB_HOST = os.environ.get("DB_HOST")
DB_PASS = os.environ.get("DB_PASS")
DB_USER = os.environ.get("DB_USER")
DB_NAME = os.environ.get("DB_NAME")



class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASS, DB_HOST, DB_NAME)
        setup_db(self.app, self.database_path)
        self.new_question = {
            'question':'Who sang Billie Jean?',
            'answer':'Micheal Jackson',
            'difficulty':1,
            'category':5
        }
        self.invalid_new_question = {
            'question':'Who sang Bohemian Rhapsody?',
            'answer':'Queen',
            'difficulty':1
        }
        self.search_questions = {
            'searchTerm': 'e'
        }

        self.new_quiz = {
            "quiz_category": {
                "id": 2,
                "type":"Science"
            },
            "previous_questions":[10]
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

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data["categories"])

    def test_get_all_questions(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

    def test_get_questions_beyond_valid_page(self):
        res = self.client().get('/questions?page=256')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data['message'],'Resource not found')
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        res = self.client().delete('/questions/25')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code,200)
        self.assertEqual(data['question_deleted'],25)


    def test_delete_invalid_question(self):
        res = self.client().delete('/questions/299')

        self.assertEqual(res.status_code,500)

    def test_post_question(self):
        res = self.client().post('/questions', json = self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,200)
        self.assertTrue(data['questions'])

    def test_post_invalid_question(self):
        res = self.client().post('/questions', json = self.invalid_new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data['message'], 'bad request')
        self.assertEqual(data['success'], False)

    def test_search_questions(self):
        res = self.client().post('/questions', json = self.search_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    def test_get_all_questions_from_category(self):
        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_get_all_questions_from_invalid_category(self):
        res = self.client().get('/categories/8/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'],'Resource not found')
        self.assertEqual(data['success'], False)

    def test_play_quizzes(self):
        res = self.client().post('/quizzes', json=self.new_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()