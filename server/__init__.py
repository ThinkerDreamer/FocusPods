from flask import Flask

def init_app():
    """Initialize the core application."""
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    print("I am being called from inside init_app in __init__.py")

    from .lib.models import db
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes
        print(routes)
        return app

# app = Flask(__name__)



# if __name__ == "__main__":
#     app.config.from_pyfile('config.py')
#     app.run(debug=True)
