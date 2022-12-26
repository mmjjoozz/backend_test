from flask import Flask

from app.db import init_db


def create_app():
    from app.urls import api

    app = Flask(__name__)

    api.init_app(app)
    init_db()

    return app
