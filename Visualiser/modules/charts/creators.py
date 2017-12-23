from enum import Enum

from bokeh.plotting import figure

from .models import Chart, ChartOptions, ChartTitle
from ..common.creators import DocumentRecipe
from ..common.models import LayerDocument


class LineRecipe(DocumentRecipe):
    """
    Recipe for creating line on a plot.
    """
    @classmethod
    def create(cls, document: LayerDocument, base_object: figure) -> None:
        """
        Create line on a plot figure.

        :param document: (LayerDocument) layer document object containing ingredients and configuration for
        creating a line.
        :param base_object: (bokeh.plotting.figure) bokeh figure to create line on
        :return: None
        """
        return cls._add_layer(plot=base_object, layer_document=document)

    @classmethod
    def _add_layer(cls, plot: figure, layer_document: LayerDocument) -> None:
        """
        Create line on a plot figure. Method creates line and adjusts it based on configuration. The line is appended to
        the provided plot.

        :param layer_document: (LayerDocument) layer document object containing ingredients and configuration for
        :param plot: (bokeh.plotting.figure) bokeh figure to create line on
        :return: None
        """
        # TODO: add support for hover tool.
        layer_model = layer_document.model
        layer_figure = layer_model.figure
        axis = layer_model.axis

        plot.yaxis.axis_label = axis.name or axis.data_field
        plot.line(layer_document.data_source[layer_document.x_axis.data_field],
                  layer_document.data_source[axis.data_field],
                  color=layer_figure.colour,
                  alpha=layer_figure.opacity)


class ChartRecipe(DocumentRecipe):
    """
    Recipe for creating a plot to display to the user.
    """

    @classmethod
    def create(cls, document: Chart) -> figure:
        """
        Create bokeh figure to display to the user.

        :param document: (Chart) chart document object containing ingredients for bokeh figure creation.
        :return plot: (bokeh.plotting.figure) bokeh figure object to display to the user.
        """
        chart_options = document.chart_options

        plot = cls._create_plot(chart_options=chart_options)
        cls._add_title(plot, chart_options.title)

        return plot

    @classmethod
    def _create_plot(cls, chart_options: ChartOptions) -> figure:
        """
        Create plot based on options provided via chart object and return it.

        :return: plot(bokeh.plotting.figure): bokeh plot figure instance customised for provided options.
        """
        x = chart_options.x_axis
        x_data_type = x.data_type or "auto"

        plot = figure(height=chart_options.height, width=chart_options.width, x_axis_type=x_data_type)
        plot.xaxis.axis_label = chart_options.x_axis.name or chart_options.x_axis.data_field

        return plot

    @staticmethod
    def _add_title(plot: figure, title: ChartTitle) -> None:
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


class ChartRecipes(Enum):
    """
    Enum class containing supported recipes for chart document factorisation.
    """
    Chart = ChartRecipe
    Line = LineRecipe

    @classmethod
    def to_list(cls) -> [Enum]:
        return [recipe for recipe in cls]
