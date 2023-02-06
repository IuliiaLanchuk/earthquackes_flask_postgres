
from flask import Flask


def create_app():

    app = Flask(__name__)

    app.config.from_object('appl.config.Config')

    # from appl.routes import init_routes
    # init_routes(app)
    return app
