from flask import Blueprint
from flask import render_template

from .controllers import HomeController
from ..common.services import Service

home = Blueprint('home', __name__)


@home.record
def record_config(setup_state):
    config = setup_state.app.config
    home.config = config
    Service.set_options(options=dict([(key, value) for (key, value) in config.items()]))


@home.route('/')
@home.route('/home')
def index():
    return render_template("home/home.html", controller=HomeController())


@home.route('/settings')
def settings():
    return render_template("home/settings.html", controller=HomeController())
