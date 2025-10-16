import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
import sqlite3

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# DATABASE
connection = sqlite3.connect("birthdays.db", check_same_thread=False)
connection.row_factory = sqlite3.Row
db = connection.cursor()

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        month = request.form.get("month")
        day = request.form.get("day")
        add_bday(name, month, day)
        return redirect("/")
    else:
        return render_template("index.html", entries=get_bdays())

def add_bday(name, month, day):
    db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", (name, month, day))
    connection.commit()

def get_bdays():
    entries = db.execute("SELECT name, month, day FROM birthdays")
    return entries.fetchall()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
