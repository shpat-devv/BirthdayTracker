import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from api.models import User, Birthday

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

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
        user = User(email, password)
        user.exists()

    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        user = User(username, email, password)
        user.save()
        
        if username == "admin" and password == "1234":
            session["user_id"] = 1
            flash("Login successful!", "success")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))

    return render_template("signup.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


@app.route("/", methods=["GET", "POST"])
def index():
    # Require login
    if "user_id" not in session:
        flash("You must be logged in to access this page.", "error")
        return redirect(url_for("login"))

    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        add_bday(name, month, day, session["user_id"])
        flash(f"Added birthday for {name}!", "success")
        return redirect("/")

    # entries = get_bdays(session["user_id"])
    return render_template("index.html")  # , entries=entries)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
