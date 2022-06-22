import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    # Formatting the questions
    fmt_questions = [question.format() for question in questions]

    current_questions = fmt_questions[start:end]

    return current_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers",
            "Content-Type:application/json, Authorization,true")
        response.headers.add(
            "Access-Control-Allow-Methods",
            "GET,PUT,POST,DELETE,OPTIONS")
        return response

    @app.route('/categories')
    def get_categories():
        # Fetch all categories from the database
        categories = Category.query.order_by(Category.id).all()
        fmt_category = {category.id: category.type for category in categories}
        return jsonify({
            'categories': fmt_category
        })

    @app.route('/questions')
    def get_questions():
        try:
            questions = Question.query.order_by(Question.id).all()
            formatted_question = paginate_questions(request, questions)

            if len(formatted_question) == 0:
                abort(404)

            else:         
                categories = Category.query.order_by(Category.id).all()
                fmt_category = {
                    category.id: category.type for category in categories}

                return jsonify({
                    'questions': formatted_question,
                    'totalQuestions': len(Question.query.all()),
                    'categories': fmt_category,
                    'currentCategory': ''
                })

        except BaseException:
            abort(404)

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.filter(
            Question.id == question_id).one_or_none()

        try:
            if question is None:
                abort(404)

            else:
                question.delete()
                return jsonify({
                    'success': True,
                    'question_deleted': question_id
                })

        except BaseException:
            abort(500)

    @app.route('/questions', methods=['POST'])
    def post_question():
        # Get the request body in json
        data = request.get_json()

        new_question = data.get('question', None)
        new_answer = data.get('answer', None)
        new_category = data.get('category', None)
        new_difficulty = data.get('difficulty', None)
        search = data.get('searchTerm', None)

        try:
            '''
            If the  searchTerm is in the request body,
            execute a search and return all questions with the search term
            '''
            if search:
                select_questions = (
                    Question.query .order_by(
                        Question.id) .filter(
                        Question.question.ilike(f'%{search}%')))

                # Paginate the questions
                current_questions = paginate_questions(
                    request, select_questions)

                return jsonify({
                    'success': True,
                    'questions': current_questions,
                    'total_questions': len(select_questions.all())
                })
            elif new_question and new_answer and new_category and new_difficulty:
                '''
                At this point the request is determined as a request
                to add a question since it does not contain a searchterm
                in the json request body
                '''
                question = Question(
                    question=new_question,
                    answer=new_answer,
                    category=new_category,
                    difficulty=new_difficulty)
                question.insert()

                questions = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, questions)

                return jsonify({
                    'questions': current_questions,
                    'totalQuestions': len(Question.query.all()),
                    'currentCategory': 'none'
                })

            else:
                abort(400)

        except BaseException:
            abort(400)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_based_on_categories(category_id):
        try:
            questions = Question.query.filter(
                Question.category == category_id).all()
            formatted_questions = paginate_questions(request, questions)

            if len(formatted_questions) == 0:
                abort(404)

            return jsonify({
                'questions': formatted_questions,
                'totalQuestions': len(Question.query.all()),
                'currentCategory': category_id
            })

        except BaseException:
            abort(404)

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        # Get the data from the request body
        data = request.get_json()

        if not data:
            abort(400)

        # Pick out quiz_category and previous_questions from the request body
        quiz_category = data.get("quiz_category")
        previous_questions = data.get("previous_questions")

        try:
            # If the player selects All in the front end,
            # the quiz_category is taken to be 0.
            # We then query questions from the database which are not in the
            # previous_questions list
            
            if quiz_category['id'] == 0:
                queriedQuestions = (
                    Question.query .filter(
                        Question.id.notin_(previous_questions)).all())
            else:
                queriedQuestions = (
                    Question.query .filter(
                        Question.category == quiz_category['id']) .filter(
                        Question.id.notin_(previous_questions)).all())

            fmt_queriedQuestions = [question.format()
                                    for question in queriedQuestions]

            # Picks a random number from the length of the list containing
            # questions to use an index
            randomIndex = random.randint(0, len(fmt_queriedQuestions) - 1)
            question = fmt_queriedQuestions[randomIndex]

            return jsonify({
                'question': question
            })

        except BaseException:
            abort(400)

    # ERROR-HANDLING

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(500)
    def bad_request(error):
        return jsonify({
            "success": False,
            'error': 400,
            "message": "internal server error"
        }), 500

    return app
