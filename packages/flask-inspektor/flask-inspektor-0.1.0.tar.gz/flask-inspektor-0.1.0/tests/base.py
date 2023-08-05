from __future__ import absolute_import

from time import sleep

from flask import Flask, Response
from flask_testing import TestCase as FlaskTestCase


class Config(object):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    @app.route("/")
    def index():
        return Response("OK")

    @app.route("/slow")
    def slow():
        sleep(0.1)
        return Response("Zzzz")

    return app


class FakeAppTestCase(FlaskTestCase):
    def create_app(self):
        return create_app()
