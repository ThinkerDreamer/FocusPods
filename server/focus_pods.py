import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, url_for, render_template, request
from markupsafe import Markup
from sqlalchemy import select
from .lib.models import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@localhost/focus_pods_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

@app.route("/users/")
def get_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/loggedin/<name>")
def logged_in(name):
    return render_template("loggedin.html", user=name)

@app.route("/sign-up/", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        user = User(name=name,
                    email=email,
                    password=password
                    )
        db.session.add(user)
        db.session.commit()
        print(f'{user} added')
        flash(f'Welcome {name}!')
        flash("You have successfully signed up!")
        flash(Markup("Please <a href='/login'>login</a> to continue"))
    return render_template("signup.html")

@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_logging_in = db.session.execute(select(User).where(User.email==email).where(User.password==password)).one_or_none()
        if user_logging_in:
            user_logging_in = dict(user_logging_in)  # Converts from Row type to Dict
            name_of_user = user_logging_in["User"].name  # Grabs the name from the Dict
            return redirect(url_for("logged_in", name=name_of_user))
        else:
            flash("Incorrect login credentials!")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/<room_id>/")
def room(room_id):
    return render_template("room.html", room_id=room_id)


if __name__ == "__main__":
    app.secret_key = "I am a super secret key!"
    app.config["SESSION_TYPE"] = 'filesystem'
    app.run(debug=True)
