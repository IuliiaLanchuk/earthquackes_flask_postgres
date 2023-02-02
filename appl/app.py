from appl import create_app
from appl.models import db

from flask_migrate import Migrate

app = create_app()
db.init_app(app)
migrate = Migrate(app, db)


if __name__ == "__main__":
    app.run(debug=True)
