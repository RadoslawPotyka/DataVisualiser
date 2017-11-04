from flask import render_template

#from Visualiser.modules.charts.controllers import ChartsController

from flask import Blueprint


charts = Blueprint('charts', __name__)


@charts.route('/home')
def index():
    return render_template("maps/home.html", controller=None)
