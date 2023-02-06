from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

app.config.from_object('appl.config.Config')
from appl import db

db.init_app(app)


def init_app():
    with app.app_context():
        # Create sql tables for our data models
        from appl.routes import page
        db.create_all()

        app.register_blueprint(page)

    return app


migrate = Migrate(app=app, db=db)

from appl import models, db

if __name__ == "__main__":
    init_app().run(debug=True)
