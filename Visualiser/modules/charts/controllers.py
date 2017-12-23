from .services import BokehService, ChartService


class ChartDisplayController(object):
    """
    Controller responsible for handling chart creation. Contains all methods necessary for creating and storing
    charts with options provided by form data and pandas data frame object with values loaded from uploaded file.

    Attributes:
        __bokeh_resources(TemplateResourcesData): standard css and js resources for bokeh charts.
        __chart_resources(TemplateResourcesData): js and html resources for particular bokeh charts.
    """

    __chart_resources = None
    __bokeh_resources = None

    def load_demo_plot(self):
        chart = ChartService.get_demo_chart()
        plot = BokehService.generate_plot(chart)

        self.__bokeh_resources = BokehService.get_bokeh_resources()
        self.__chart_resources = BokehService.export_plot(plot)

    @property
    def chart_resources(self):
        return self.__chart_resources

    @property
    def bokeh_resources(self):
        return self.__bokeh_resources
