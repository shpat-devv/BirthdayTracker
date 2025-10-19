import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from api.models import User, Birthday, verify

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config.update(
    TESTING=True,
    SECRET_KEY='192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf'
)
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print(f"checking {email}, {password}")
        user = User("temp", email, password) #temporary username, will be changed once the user is verified
        if user.exists():
            return render_template("login.html", user_id = user.get_id)
        else:
            return render_template("login.html", response = "Failed")

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User(username, email, password)
        try:
            user.save()
            return render_template("signup.html", response = "Valid")
        except Exception as e:
            print(f"Error: {e}")
            return render_template("signup.html", response = "Failed")

        

    return render_template("signup.html")


@app.route("/", methods=["GET", "POST"])
def index():
    # Require login
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")

        print(f"Saving birthday for {name} on {month, day}")
        return redirect("/")

    # entries = get_bdays(session["user_id"])
    return render_template("index.html")  # , entries=entries)


@app.route("/validate", methods=["POST"])
def validate():
    user_id = request.form.get("id")

    if not user_id:
        return jsonify({"valid": False}), 400

    if verify(user_id):
        return jsonify({"valid": True}), 200
    else:
        return jsonify({"valid": False}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
