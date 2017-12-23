from enum import Enum

from ..common.models import Document, DocumentOptions, ObjectKey


class ChartTitle(object):
    """
    Object representing title for a chart. Has it's title, colour string, font string and styling.

    Attributes:
        @property title(str): actual title of the chart
        @property colour(str): colour of the title
        @property font(str): font used for title
        @property font_style(str): font styling for the title
    """

    def __init__(self):
        self.__title = None
        self.__colour = None
        self.__font = None
        self.__font_style = None

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title: str):
        self.__title = title

    @property
    def colour(self):
        return self.__colour

    @colour.setter
    def colour(self, colour: str):
        self.__colour = colour

    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, font: str):
        self.__font = font

    @property
    def font_style(self):
        return self.__font_style

    @font_style.setter
    def font_style(self, font_style: str):
        self.__font_style = font_style


class ChartOptions(DocumentOptions):
    """
    Represents chart configuration for data visualisation. Contains useful information and data
    for chart creation and customisation.

    Attributes:
        @property id(int): chart id for identyfying particular chart
        @property width(int): width of the chart in pixels
        @property height(int): height of the chart in pixels
        @property description(str): description of the chart
        @property x_axis(Axis): Axis class instance for determining values and display of X axis of the chart
        @property title(ChartTitle): Title class instance containing styling and display of chart title
        @property layers(list(ChartFigure)): List of all layers to be displayed on chart.
    """

    __DEFAULT_SIZE = 500

    def __init__(self):
        super().__init__()
        self.__width = self.__DEFAULT_SIZE
        self.__height = self.__DEFAULT_SIZE
        self.__title = ChartTitle()

    @property
    def width(self) -> int:
        return self.__width

    @width.setter
    def width(self, width: int):
        self.__width = width

    @property
    def height(self) -> int:
        return self.__height

    @height.setter
    def height(self, height: int):
        self.__height = height

    @property
    def title(self) -> ChartTitle:
        return self.__title

    @title.setter
    def title(self, title: ChartTitle):
        self.__title = title


class Chart(Document):
    """
    Represents whole chart object ready to display. Wraps chart configuration and its data source for easier
    transportation throughout solution and its services.

    Attributes:
        @property chart_options(ChartOptions): chart configuration object for the chart.
        @property data_source(pandas.DataFrame): data source used in the chart.
    """

    _object_key = ObjectKey.Chart

    def __init__(self):
        super().__init__()
        self._model = None
        self._data_source = None

    @property
    def chart_options(self) -> ChartOptions:
        return self._model

    @chart_options.setter
    def chart_options(self, chart_options: ChartOptions):
        self._model = chart_options
