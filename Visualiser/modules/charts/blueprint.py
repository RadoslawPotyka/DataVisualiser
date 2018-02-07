from flask import render_template, request

from .controllers import ChartDisplayController, ChartCreateController, ChartEditController

from flask import Blueprint

charts = Blueprint('charts', __name__)
charts.config = {}


@charts.record
def record_config(setup_state):
    config = setup_state.app.config
    charts.config = config


@charts.route('/home')
def index():
    return render_template("charts/home.html", controller=None)


@charts.route('/preview')
def preview():
    controller = ChartDisplayController()
    controller.load_demo_plot()

    return render_template("charts/preview.html", controller=controller)


@charts.route('/create', methods=['GET', 'POST'])
def create():
    controller = ChartCreateController(template_path="charts/display.html")
    return controller.activate(is_empty=False)


@charts.route('/edit', methods=['GET', 'POST'])
def edit():
    is_empty = request.method != 'POST'
    controller = ChartEditController(template_path="charts/edit.html")

    return controller.activate(is_empty=is_empty)
