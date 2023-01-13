from flask import url_for, render_template, redirect, flash, session, request
from markupsafe import Markup
from sqlalchemy import select
import uuid
import json
from . import start_app
from .lib.models import db, Room, room_user, User, Invite

app = start_app()

# For testing purposes only, show all users
@app.route("/users/")
def get_users():
    users = User.query.all()
    return render_template("users.html", users=users)


# For testing purposes only, show all rooms
@app.route("/rooms/")
def get_rooms():
    rooms = Room.query.all()
    return render_template("rooms.html", rooms=rooms)


# Home page
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/sign-up/", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        user = User(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        print(f"{user} added")
        flash(f"Welcome {name}!")
        flash("You have successfully signed up!")
        flash(Markup("Please <a href='/login'>login</a> to continue"))
    return render_template("signup.html")


@app.route("/login/", methods=["POST", "GET"])
def login():
    if session:
        session.clear()
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user_logging_in = db.session.execute(
            select(User).where(User.email == email).where(User.password == password)
        ).one_or_none()
        if user_logging_in:
            session["logged_in"] = True
            user_logging_in = dict(user_logging_in)  # Converts from Row type to Dict
            name_of_user = user_logging_in["User"].name  # Grabs the name from the Dict
            user_id = user_logging_in["User"].id  # Grab the id
            session["name"] = name_of_user
            session["uid"] = user_id
            return redirect(url_for("logged_in"))
        else:
            flash("Incorrect login credentials!")
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/loggedin/", methods=["POST", "GET"])
def logged_in():
    name = session.get("name", None)
    id = session.get("uid", None)
    pods_user_is_in = (
        Room.query.join(room_user)
        .join(User)
        .filter((room_user.c.user_id == id) & (room_user.c.room_id == Room.id))
        .all()
    )
    all_rooms = Room.query.all()
    pod_list = []
    for room in all_rooms:
        for pod in pods_user_is_in:
            if room.id == pod.id:
                pod_list.append(room)
    top_message = "You are now logged in!"

    # Create a room
    if request.method == "POST":
        user_id = session["uid"]
        room_name = request.form["room_name"]
        owner_row = db.session.execute(
            select(User).where(User.id == user_id)
        ).one_or_none()

        # Create the room without many-to-many user list first
        room = Room(name=room_name, owner=owner_row.User.id)
        db.session.add(room)

        # After adding the room to the schema, add the owner to the users list
        room.users.append(owner_row.User)
        db.session.commit()
        pod_list.append(room)
        top_message = "You have successfully created a pod!"
        return render_template(
            "loggedin.html", user=name, pods=pod_list, top_message=top_message
        )

    return render_template(
        "loggedin.html", user=name, pods=pod_list, top_message=top_message
    )


@app.route("/logout/")
def logout():
    if session["logged_in"] == True:
        session.clear()
        return render_template("loggedout.html")
    else:
        return render_template("not_logged_in.html")


@app.route("/pod/<room_id>/")
def room(room_id):
    user = session.get("name", None)
    room_row = db.session.execute(select(Room).where(Room.id == room_id)).one_or_none()
    occupants = room_row.Room.users
    session["room_id"] = room_id
    return render_template(
        "room.html", room_id=room_id, user=user, room=room_row, occupants=occupants
    )


@app.route("/invite/", methods=["POST", "GET"])
def invite():
    user_id = session.get("uid", None)
    room_id = session.get("room_id", None)
    if request.method == "POST":
        jsonData = request.get_json()
        print(f"jsonData is {jsonData}")
        return {"response": "I am the response"}
        invitation = Invite(user_id=user_id, room_id=room_id, link_id=uuid.uuid4())
        db.session.add(invitation)
        db.session.commit()
        print(f"{invitation} added")
        # invitation_row = db.session.execute(
        #     select(Invite)
        #     .where(Invite.user_id == user_id)
        #     .where(Invite.room_id == room_id)
        # ).one_or_none()
        # Convert from Row type to Dict
        invitation_dict = dict(invitation)
        # Grab the name from the Dict
        invitation_code = invitation_dict["Invite"].link_id
        return render_template(url_for("invite"), link_id=invitation_code)
    else:
        return render_template("invitation.html")
