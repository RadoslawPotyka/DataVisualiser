from .services import BokehService, ChartService


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
