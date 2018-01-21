from flask import Flask, redirect, url_for

from .modules.home.blueprint import home
from .modules.maps.blueprint import maps
from .modules.charts.blueprint import charts
from .config import *

app = Flask(__name__, static_url_path="/static", static_folder="static")

app.config.from_object(TestingConfig)

app.register_blueprint(blueprint=home, url_prefix='/app')
app.register_blueprint(blueprint=maps, url_prefix='/app/maps')
app.register_blueprint(blueprint=charts, url_prefix='/app/charts')


@app.route("/")
def index():
    return redirect(url_for('home.index'))
