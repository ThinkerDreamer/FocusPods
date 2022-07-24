import os
from flask import Flask, flash, redirect, session, url_for, render_template, request, session
from markupsafe import Markup
from flask_sqlalchemy import BaseQuery, SQLAlchemy
from sqlalchemy import Column, ForeignKey, Table, select, Integer
from sqlalchemy import func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@localhost/focus_pods_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

association_table = Table(
    "association",
    Base.metadata,
    Column("room_id", ForeignKey("rooms.id")),
    Column("user_id", ForeignKey("users.id")),
)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    children = relationship("Room", secondary=association_table)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, email={self.email!r}, created_at={self.created_at!r})"

class Room(db.Model):
    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, name={self.name!r}, created_at={self.created_at!r})"


@app.route("/users/")
def get_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/loggedin/<name>")
def logged_in(name):
    return render_template("loggedin.html", user=name, )

@app.route("/sign-up/", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        user = User(name=name,
                    email=email,
                    password=password,
                    created_at= func.now(),
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
        username = request.form["username"]
        password = request.form["password"]
        result = db.session.execute(select(User).where(User.email==username).where(User.password==password)).all()
        print("do we see this?", result)
        if result:
            session["logged_in"] = True
            return redirect(url_for("logged_in", name=username))

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
