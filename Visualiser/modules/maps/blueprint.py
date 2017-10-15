from flask import render_template

from Visualiser.modules.maps.controllers import MapsController

from flask import Blueprint


maps = Blueprint('maps', __name__)


@maps.route('/home')
def index():
    return render_template("maps/home.html", controller=MapsController())
