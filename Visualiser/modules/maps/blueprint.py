from flask import render_template, request

from .controllers import MapCreateController, MapEditController

from flask import Blueprint


maps = Blueprint('maps', __name__)


@maps.route('/home')
def index():
    return render_template("maps/home.html")


@maps.route('/preview')
def preview():
    return render_template("maps/home.html")


@maps.route('/create', methods=['GET', 'POST'])
def create():
    controller = MapCreateController(template_path="maps/display.html")
    return controller.activate(is_empty=False)


@maps.route('/edit', methods=['GET', 'POST'])
def edit():
    is_empty = request.method != 'POST'
    controller = MapEditController(template_path="maps/edit.html")
    return controller.activate(is_empty=is_empty)
