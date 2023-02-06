from flask_sqlalchemy import SQLAlchemy

from appl import create_app


from flask_migrate import Migrate

app = create_app()

db = SQLAlchemy()
db.init_app(app)


def init_app():
    from appl.routes import init_routes
    init_routes(app)
    with app.app_context():
        db.create_all()

    return app


migrate = Migrate(app=app, db=db)

from appl import models


if __name__ == "__main__":
    init_app().run(debug=True)
