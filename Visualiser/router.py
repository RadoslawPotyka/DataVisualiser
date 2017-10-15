from Visualiser import app
from flask import render_template, url_for


@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")


@app.route('/settings')
def settings():
    # TODO: user info fetching
    user = None
    return render_template("settings.html", user=user)
