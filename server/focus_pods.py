import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, flash, redirect, session, url_for, render_template, request
from markupsafe import Markup
from sqlalchemy import select
from .lib.models import Room, room_user, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://{os.environ["DB_USERNAME"]}:{os.environ["DB_PASSWORD"]}@localhost/focus_pods_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# For testing purposes only, show all users
@app.route("/users/")
def get_users():
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route("/")
def home():
    return render_template("index.html")

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
    if session:
        session.clear()
        print(session)
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_logging_in = db.session.execute(select(User).where(User.email==email).where(User.password==password)).one_or_none()
        if user_logging_in:
            session["logged_in"] = True
            user_logging_in = dict(user_logging_in)  # Converts from Row type to Dict
            name_of_user = user_logging_in["User"].name  # Grabs the name from the Dict
            print(f'name_of_user is: {name_of_user}')
            user_id = user_logging_in["User"].id  # Grab the id
            session["name"] = name_of_user
            print(f'session["name"] is: {session["name"]}')
            session["uid"] = user_id
            return redirect(url_for("logged_in"))
        else:
            flash("Incorrect login credentials!")
            return render_template("login.html")
    else:
        return render_template("login.html")

@app.route("/loggedin/")
def logged_in():
    name = session.get("name", None)
    id = session.get("uid", None)
    pods_user_is_in = Room.query.join(room_user).join(User).filter((room_user.c.user_id == id) & (room_user.c.room_id == Room.id)).all()

    print(f'pods_user_is_in is: {pods_user_is_in}')
    all_rooms = Room.query.all()
    pod_list = []
    for room in all_rooms:
        for pod in pods_user_is_in:
            if room.id == pod.id:
                pod_list.append(room)
    print(f"pods is: {pods_user_is_in}")
    print(f"pod_list is: {pod_list}")
    return render_template("loggedin.html", user=name, pods=pod_list)

@app.route("/logout/")
def logout():
    if session["logged_in"] == True:
        session.clear()
        return render_template("loggedout.html")
    else:
        return render_template("not_logged_in.html")

# @app.route("/<room_id>/")
# def room(room_id):
#     return render_template("room.html", room_id=room_id)


if __name__ == "__main__":
    app.secret_key = "I am a super secret key!"
    app.config["SESSION_TYPE"] = 'filesystem'
    app.run(debug=True)
