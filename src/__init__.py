from datetime import timedelta

from flask import Flask, jsonify
import os
from src.services.AuthServices import auth
from src.services.EmployeeServices import employee
from src.services.StatisticsServices import statistics
from src.services.ApplicationServices import application
from src.models.Database import db
from flask_jwt_extended import JWTManager
from src.constants.http_status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from flask_cors import CORS, cross_origin


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    CORS(app) # This will enable CORS for all routes
    app.config['JSON_SORT_KEYS'] = False
    app.app_context().push()

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get('JWT_SECRET_KEY'),
            JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30),
            JWT_REFRESH_TOKEN_EXPIRES=timedelta(days=30)
        )
    else:
        app.config.from_mapping(test_config)

    # db initiating 
    db.app = app
    db.init_app(app)
    JWTManager(app)

    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({'ERROR': 'NOT FOUND'}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return jsonify({'ERROR': 'SORRY, SOMETHING WENT WRONG, WE ARE WORKING ON IT'}), HTTP_500_INTERNAL_SERVER_ERROR

    app.register_blueprint(auth)
    app.register_blueprint(employee)
    app.register_blueprint(statistics)
    app.register_blueprint(application)

    return app
