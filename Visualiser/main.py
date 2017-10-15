from flask import Flask

from Visualiser.modules.main.blueprint import home
from Visualiser.modules.maps.blueprint import maps

app = Flask(__name__)

app.register_blueprint(blueprint=home, url_prefix='/app')
app.register_blueprint(blueprint=maps, url_prefix='/app/maps')
