# TODO: generate chart adjustments, move to controllers?
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import CDN

from Visualiser.modules.common.models import TemplateResourcesData
from .models import Chart


class BokehService(object):
    """
    Static service handling Bokeh chart generation and export.
    """

    @staticmethod
    def generate_plot(data_frame, chart_options):
        """
        Generate plot for given pandas DataFrame and chart options. Returns created plot object

        :param data_frame: (pd.DataFrame) pandas DataFrame object containing values to display on a plot.
        :param chart_options: (Chart) options for a chart display and shapes.
        :return plot: (bokeh.plotting.figure) bokeh plot object
        """
        chart_creator = ChartCreator(pandas_data_frame=data_frame, chart=chart_options)
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
        template_resources.js_list = CDN.js_files
        template_resources.css_list = CDN.css_files

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
        template_resources.js_list, template_resources.html_list = components(plot)

        return template_resources


class ChartCreator(object):
    """
    Handles generation of the bokeh chart using chart options and pandas data frame provided during initialisation.

    Args:
                pandas_data_frame(pd.DataFrame): pandas DataFrame object instance containing columns to display on the
                chart.
                chart(Chart): Chart object instance containing all options for chart customisation and display
    """

    def __init__(self, pandas_data_frame, chart):
        self.__data_frame = pandas_data_frame
        self.__chart_options = chart
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
            plot.yaxis.axis_label = layer.axis.name
            plot.getattr(plot, layer_figure.shape)(self.__data_frame[self.__x_axis_data_field],
                                                   self.__data_frame[axis.data_field],
                                                   color=layer_figure.color,
                                                   alpha=layer_figure.opacity)
        return plot

    def __create_plot(self):
        """
        Create plot based on options provided via chart object and return it.

        :param chart(Chart): Chart object instance containing options for bokeh plot creation.
        :return: plot(bokeh.plotting.figure): bokeh plot figure instance customised for provided options.
        """
        chart = self.__chart_options

        x = chart.x_axis
        x_data_type = x.data_type | "string"

        plot = figure(height=chart.height, width=chart.width, x_axis_type=x_data_type, responsive=True)
        plot.xaxis.axis_label = chart.x_axis.name | chart.x_axis.data_field
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
        plot.title = title.title
        plot.title_text_color = title.colour | 'black'
        plot.title_text_font = title.font | "times"
        plot.title_text_font_style = title.font_style
