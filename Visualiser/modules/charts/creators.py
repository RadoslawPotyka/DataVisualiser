from enum import Enum
from abc import abstractmethod

from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource

from .models import Chart, ChartOptions, ChartTitle, ChartLayerDocument
from ..common.creators import DocumentRecipe, DocumentFactory
from ..common.models import Layer, Axis


class HoverToolRecipe(DocumentRecipe):
    """
    Recipe for creating hover tool on the plot.
    """

    @classmethod
    def create(cls, document: Chart, base_object: figure) -> None:
        """
        Create a hover tool for a plot.

        :param document: (Chart) chart document object instance.
        :param base_object: (bokeh.plotting.figure) bokeh figure to create hover tool for.
        :return: None
        """
        chart_options = document.chart_options
        layers = chart_options.layers

        return cls._add_hover_tool(chart_layers=layers, plot=base_object)

    @classmethod
    def _add_hover_tool(cls, chart_layers: [Layer], plot: figure) -> [tuple]:
        """
        Add hover tool to a bokeh plot. Method iterates through chart layers to create a hover tool tooltip for each of
        them based on axis of the layer.

        :param chart_layers:  list(Layer) list of layers to prepare tooltips for.
        :param plot: bokeh.plotting.figure) bokeh figure to create hover tool for.
        :return:
        """
        tooltips = []

        for layer in chart_layers:
            axis = layer.axis
            cls._prepare_tooltip(tooltips=tooltips, axis=axis)

        if len(tooltips) > 0:
            hover_tool = HoverTool(tooltips=tooltips)
            plot.add_tools(hover_tool)

    @classmethod
    def _prepare_tooltip(cls, tooltips: [tuple], axis: Axis) -> None:
        """
        Prepares tooltip tuple for a given axis and appends it to provided tooltips list.

        :param tooltips: list(tuple) list of tuples containing tooltips for a plot.
        :param axis: (Axis) axis of a layer to prepare tooltip tuple for.
        :return: None
        """
        tooltip_data = '@{0}'.format(axis.data_field)
        tooltip_label = axis.name
        tooltip = (tooltip_label, tooltip_data)

        tooltips.append(tooltip)


class LayerRecipe(DocumentRecipe):
    """
    Base interface for layer recipe.
    """

    @classmethod
    def create(cls, document: ChartLayerDocument, base_object: figure) -> None:
        """
        Create a layer on a plot figure. Method creates layer and adjusts it based on configuration.
        The layer is appended to the provided plot.

        :param document: (LayerDocument) layer document object containing ingredients and configuration for
        creating a line.
        :param base_object: (bokeh.plotting.figure) bokeh figure to create line on
        :return: None
        """
        return cls._add_layer(plot=base_object, layer_document=document)

    @classmethod
    @abstractmethod
    def _add_layer(cls, plot: figure, layer_document: ChartLayerDocument) -> None:
        pass


class LineRecipe(LayerRecipe):
    """
    Recipe for creating line on a plot.
    """

    @classmethod
    def _add_layer(cls, plot: figure, layer_document: ChartLayerDocument) -> None:
        """
        Create line on a plot figure. Method creates line and adjusts it based on configuration. The line is appended to
        the provided plot.

        :param layer_document: (LayerDocument) layer document object containing ingredients and configuration for
        :param plot: (bokeh.plotting.figure) bokeh figure to create line on
        :return: None
        """
        layer_model = layer_document.model
        layer_figure = layer_model.figure

        axis = layer_model.axis
        axis.name = axis.name or axis.data_field
        plot.yaxis.axis_label = axis.name

        plot.line(layer_document.x_axis.data_field,
                  axis.data_field,
                  color=layer_figure.colour,
                  alpha=layer_figure.opacity,
                  legend=axis.name,
                  line_width=layer_figure.size,
                  source=layer_document.data_source)


class CircleRecipe(LayerRecipe):
    """
    Recipe for creating a circle on a plot.
    """

    @classmethod
    def _add_layer(cls, plot: figure, layer_document: ChartLayerDocument) -> None:
        """
        Create circle on a plot figure. Method creates circle and adjusts it based on configuration. The circle is
        appended to the provided plot.

        :param layer_document: (LayerDocument) layer document object containing ingredients and configuration for
        :param plot: (bokeh.plotting.figure) bokeh figure to create circle on
        :return: None
        """
        layer_model = layer_document.model
        layer_figure = layer_model.figure

        axis = layer_model.axis
        axis.name = axis.name or axis.data_field
        plot.yaxis.axis_label = axis.name

        plot.yaxis.axis_label = axis.name or axis.data_field
        plot.circle(layer_document.x_axis.data_field,
                    axis.data_field,
                    color=layer_figure.colour,
                    alpha=layer_figure.opacity,
                    legend=axis.name,
                    size=layer_figure.size,
                    source=layer_document.data_source)


class SquareRecipe(LayerRecipe):
    """
    Recipe for creating square on a plot.
    """

    @classmethod
    def _add_layer(cls, plot: figure, layer_document: ChartLayerDocument) -> None:
        """
        Create square on a plot figure. Method creates square and adjusts it based on configuration.
        The square is appended to the provided plot.

        :param layer_document: (LayerDocument) layer document object containing ingredients and configuration for
        :param plot: (bokeh.plotting.figure) bokeh figure to create square on
        :return: None
        """
        layer_model = layer_document.model
        layer_figure = layer_model.figure

        axis = layer_model.axis
        axis.name = axis.name or axis.data_field

        plot.yaxis.axis_label = axis.name
        plot.square(layer_document.x_axis.data_field,
                    axis.data_field,
                    color=layer_figure.colour,
                    alpha=layer_figure.opacity,
                    legend=axis.name,
                    size=layer_figure.size,
                    source=layer_document.data_source)


class ChartRecipe(DocumentRecipe):
    """
    Recipe for creating a plot to display to the user.
    """

    post_execute = HoverToolRecipe

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
        x_data_type = x.data_type

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
    Circle = CircleRecipe
    Square = SquareRecipe


class ChartFactory(DocumentFactory):
    """
    Chart specific DocumentFactory containing all necessary methods and overridings for proper chart factorisation.
    """

    def prepare_layer_document(self, layer: Layer, document: Chart) -> ChartLayerDocument:
        """
        Prepares LayerDocument object for creating layer on a chart.

        :param layer: (Layer) layer configuration object.
        :param document: (Chart) chart document to append LayerDocument to.
        :return layer_document: (ChartLayerDocument) prepared layer document to append on a document.
        """
        layer_data_source = self.prepare_layer_data_source(data_source=document.data_source,
                                                           filter_expression=layer.filter_expression)
        layer_data_source = ColumnDataSource(layer_data_source)

        layer_document = ChartLayerDocument(layer=layer, data_source=layer_data_source, x_axis=document.model.x_axis)
        return layer_document

    def validate(self, document: Chart) -> None:
        super().validate(document=document)
