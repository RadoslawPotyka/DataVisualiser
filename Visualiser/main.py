from flask import Flask, redirect, url_for

from Visualiser.modules.home.blueprint import home
from Visualiser.modules.maps.blueprint import maps
from Visualiser.modules.charts.blueprint import charts

app = Flask(__name__)

app.register_blueprint(blueprint=home, url_prefix='/app')
app.register_blueprint(blueprint=maps, url_prefix='/app/maps')
app.register_blueprint(blueprint=charts, url_prefix='/app/charts')


@app.route("/")
def index():
    return redirect(url_for('home.index'))
