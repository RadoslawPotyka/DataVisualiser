from Visualiser import app
from flask import render_template, url_for


@app.route('/')
@app.route('/home')
def home():
    return "Home page"
