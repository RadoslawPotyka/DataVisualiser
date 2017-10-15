from flask import Blueprint
from flask import render_template

from Visualiser.modules.main.controllers import HomeController


home = Blueprint('home', __name__)


@home.route('/')
@home.route('/home')
def index():
    return render_template("home/home.html", controller=HomeController())


@home.route('/settings')
def settings():
    # TODO: user info fetching
    return render_template("home/settings.html", controller=HomeController())


# @home.route('/maps')
# def maps_list():
#     # TODO: maps info fetching
#     return render_template("maps/home.html", controller=MapsController())
