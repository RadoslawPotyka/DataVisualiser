from .services import BokehService, ChartCreator
from .models import Chart, ChartLayer
import pandas as pd
from bokeh.plotting import figure


class ChartDisplayController(object):
    """
    Controller responsible for handling chart creation. Contains all methods necessary for creating and storing
    charts with options provided by form data and pandas data frame object with values loaded from uploaded file.
    """
    chart_data = Chart()

    def __init__(self):
        pass

    def __load_chart(self):
        pass
