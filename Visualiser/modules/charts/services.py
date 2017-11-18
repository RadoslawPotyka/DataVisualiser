from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import CDN

from ..common.models import TemplateResourcesData
from .models import Chart
from .tests.test_samples import ChartSampleGenerator


class ChartService(object):
    """
    Service handling all basic operations on charts like fetching or saving them.
    """

    @staticmethod
    def get_chart(chart_id=None):
        """
        Returns chart configuration object for a chart with given id. Communicates with external database api to fetch
        chart.
        :param chart_id: (int) id of a chart that should be returned. If none provided will return the demo chart.
        :return:
        """
        if chart_id is None:
            return ChartService.__get_demo_chart()
        else:
            raise ConnectionError("No external service implemented.")

    @staticmethod
    def __get_demo_chart():
        """
        Returns the demo chart generated from test_samples.

        :return chart: (Chart) chart object configuration for demo chart.
        """
        chart = ChartSampleGenerator.create_chart()
        return chart


class BokehService(object):
    """
    Static service handling Bokeh chart generation and export.
    """

    @staticmethod
    def generate_plot(chart):
        """
        Generate plot for given pandas DataFrame and chart options. Returns created plot object

        :param chart: (Chart) options for a chart display and shapes.
        :return plot: (bokeh.plotting.figure) bokeh plot object
        """
        chart_creator = ChartCreator(chart=chart)
        plot = chart_creator.generate_chart()

        return plot

    @staticmethod
    def get_bokeh_resources():
        """
        Get meta resources for bokeh plots. Returns object containing lists of all necessary links and scripts to
        display and embed bokeh chart.

        :return template_resources: (TemplateResourcesData) object containing list of resources for bokeh plots.
        """
        template_resources = TemplateResourcesData()
        template_resources.js = CDN.js_files[0]
        template_resources.css = CDN.css_files[0]

        return template_resources

    @staticmethod
    def export_plot(plot):
        """
        Export plot data. Returns object containing list of all files necessary for embedding the plot data. Does not
        contain meta data for bokeh plots.
        :param plot: (bokeh.plotting.figure) bokeh figure object to export resources from.
        :return template_resources: (TemplateResourcesData) object containing lists of all resources for provided plot.
        """
        template_resources = TemplateResourcesData()
        template_resources.js, template_resources.html = components(plot)

        return template_resources


class ChartCreator(object):
    """
    Handles generation of the bokeh chart using chart options and pandas data frame provided during initialisation.

    Args:
                chart(Chart): Chart object instance containing all options for chart and data source being used by it.
    """

    def __init__(self, chart):
        self.__data_frame = chart.data_source
        self.__chart_options = chart.chart_options
        self.__x_axis_data_field = None

    def generate_chart(self, is_proportional=True):
        """
        Method generates plot for a chart and then iterates through list of layers provided in chart object to display
        figures on generated plot

        :param is_proportional: boolean value determining whether values on both Y and X axis of the chart are
        proportional and scaled properly. If False is provided chart creator should scale those values for best possible
        display.
        :return: plot bokeh.plotting.figure): bokeh plot ready to display.
        """
        if not is_proportional:
            pass
            # TODO: make chart scalable for provided data
        plot = self.__create_plot()
        layers = self.__chart_options.layers

        for layer in layers:
            layer_figure = layer.figure
            axis = layer.axis
            plot.yaxis.axis_label = axis.description or axis.data_field
            getattr(plot, layer_figure.shape)(self.__data_frame[self.__x_axis_data_field],
                                              self.__data_frame[axis.data_field],
                                              color=layer_figure.colour,
                                              alpha=layer_figure.opacity)
        return plot

    def __create_plot(self):
        """
        Create plot based on options provided via chart object and return it.

        :return: plot(bokeh.plotting.figure): bokeh plot figure instance customised for provided options.
        """
        chart = self.__chart_options

        x = chart.x_axis
        x_data_type = x.data_type or "auto"

        plot = figure(height=chart.height, width=chart.width, x_axis_type=x_data_type)
        plot.xaxis.axis_label = chart.x_axis.description or chart.x_axis.data_field
        self.__x_axis_data_field = chart.x_axis.data_field
        self.__add_title(plot, chart.title)

        return plot

    @staticmethod
    def __add_title(plot, title):
        """
        Add title to bokeh plot based on data provided via ChartTitle object. Changes plot object in place.

        :param plot(bokeh.plotting.figure): bokeh plot to add title data to.
        :param title(ChartTitle): object containing options for a bokeh plot title.
        :return: None
        """
        plot.title.text = title.title
        plot.title.text_color = title.colour
        plot.title.text_font = title.font
        plot.title.text_font_style = title.font_style
