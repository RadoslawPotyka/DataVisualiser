from .services import BokehService, ChartService
from .models import Chart


class ChartBaseEditorController(object):
    """
    Controller responsible for base steps of creation process.

    Args:
                request(request): request used for chart creation.

    Attributes:
        __request(request): request used for creation of the chart.
        __form(wtforms.Form): Current form instance to gather data.
        __chart(Chart): Chart instance awaiting creation.
    """

    __request = None
    __form = None
    __chart = None

    def __init__(self, request):
        self.__request = request

    @property
    def form(self):
        return self.__form

    @form.setter
    def form(self, form):
        self.__form = form

    @property
    def chart(self):
        return self.__chart

    @chart.setter
    def chart(self, chart):
        self.__chart = chart


class ChartDisplayController(object):
    """
    Controller responsible for handling chart creation. Contains all methods necessary for creating and storing
    charts with options provided by form data and pandas data frame object with values loaded from uploaded file.
    """

    def __init__(self, chart_id=None):
        chart = ChartService.get_chart(chart_id=chart_id)
        plot = BokehService.generate_plot(chart)

        self.bokeh_resources = BokehService.get_bokeh_resources()
        self.chart_resources = BokehService.export_plot(plot)
