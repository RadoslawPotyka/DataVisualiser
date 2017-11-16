from flask import render_template

from Visualiser.modules.charts.controllers import ChartDisplayController

from flask import Blueprint


charts = Blueprint('charts', __name__)


@charts.route('/home')
def index():
    return render_template("charts/home.html", controller=None)


@charts.route('/preview')
def preview():
    return render_template("charts/preview.html", controller=ChartDisplayController())
