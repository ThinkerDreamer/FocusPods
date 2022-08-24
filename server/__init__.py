from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()

def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_pyfile('config.py')
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes
        return app

# app = Flask(__name__)



# if __name__ == "__main__":
#     app.config.from_pyfile('config.py')
#     app.run(debug=True)
