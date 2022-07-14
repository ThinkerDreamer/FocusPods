from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/loggedin/<name>")
def logged_in(name):
    return render_template("loggedin.html", user=name)

@app.route("/sign-up/", methods=["POST", "GET"])
def sign_up():
    return render_template("signup.html")
 
@app.route("/login/", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = request.form["name"]
        return redirect(url_for("logged_in", name=user))
    else:
        return render_template("login.html")
 
if __name__ == "__main__":
    app.run(debug=True)