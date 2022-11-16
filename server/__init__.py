from flask import Flask


def start_app():
    """Initialize the core application."""

    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    print("I am being called from inside start_app in __init__.py")

    from .lib.models import db

    db.init_app(app)

    with app.app_context():
        # Include our Routes
        print("I'm inside the app_context!")
        from . import routes

        print(routes)
        return app
