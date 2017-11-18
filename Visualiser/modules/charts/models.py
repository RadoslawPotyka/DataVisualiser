class Chart(object):
    """
    Represents whole chart object ready to display. Wraps chart configuration and its data source for easier
    transportation throughout solution and its services.

    Attributes:
        @property chart_options(ChartOptions): chart configuration object for the chart.
        @property data_source(pandas.DataFrame): data source used in the chart.
    """

    def __init__(self):
        self.__chart_options = None
        self.__data_source = None

    @property
    def chart_options(self):
        return self.__chart_options

    @chart_options.setter
    def chart_options(self, chart_options):
        self.__chart_options = chart_options

    @property
    def data_source(self):
        return self.__data_source

    @data_source.setter
    def data_source(self, data_source):
        self.__data_source = data_source


class ChartOptions(object):
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
        self.__id = None
        self.__description = None
        self.__width = self.__DEFAULT_SIZE
        self.__height = self.__DEFAULT_SIZE
        self.__X_axis = Axis()
        self.__layers = []
        self.__title = ChartTitle()

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id):
        self.__id = new_id

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, name):
        self.__description = name

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    @property
    def x_axis(self):
        return self.__X_axis

    @x_axis.setter
    def x_axis(self, axis):
        self.__X_axis = axis

    @property
    def layers(self):
        return self.__layers

    @layers.setter
    def layers(self, layers):
        self.__layers = layers

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, title):
        self.__title = title


class ChartLayer(object):
    """
    Object representation of a chart layer covering the Y axis settings and figure to display.

    Attributes:
        @property axis(Axis): Axis class instance for determining values and display of Y axis of the chart layer.
        @property figure(ChartFigure): ChartFigure class instance containing options for shape to be displayed on the
        chart layer.
    """

    def __init__(self):
        self.__axis = None
        self.__figure = None

    @property
    def axis(self):
        return self.__axis

    @property
    def figure(self):
        return self.__figure

    @axis.setter
    def axis(self, axis):
        self.__axis = axis

    @figure.setter
    def figure(self, figure):
        self.__figure = figure


class Axis(object):
    """
    Object representation of an axis containing options necessary for controlling axis on a chart.

    @property description(str): display description of an axis.
    @property data_field(str): column description used for an axis.
    @property data_type(str): data type used for an axis.
    """

    def __init__(self):
        self.__data_field = None
        self.__name = None
        self.__data_type = None

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def data_field(self):
        return self.__data_field

    @data_field.setter
    def data_field(self, data_field):
        self.__data_field = data_field

    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type):
        self.__data_type = data_type


class ChartFigure(object):
    """
    Object representation of a figure on a plot. Contains data necessary for customising point, lines and other
    geometrical shapes on a plot.

    Attributes:
        @property shape(str): Shape of the figure f.e. 'line' or 'circle'.
        @property colour(str): Colour of the figure. Can be string description or code for a colour.
        @property opacity(str): Determines transparency of the figure.
        @property size(str): Determines width of the figure on the plot in pixels.
    """

    def __init__(self):
        self.__shape = None
        self.__colour = None
        self.__opacity = None
        self.__size = None

    @property
    def shape(self):
        return self.__shape

    @shape.setter
    def shape(self, shape):
        self.__shape = shape

    @property
    def colour(self):
        return self.__colour

    @colour.setter
    def colour(self, colour):
        self.__colour = colour

    @property
    def opacity(self):
        return self.__opacity

    @opacity.setter
    def opacity(self, opacity):
        self.__opacity = opacity

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size


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
    def title(self, title):
        self.__title = title

    @property
    def colour(self):
        return self.__colour

    @colour.setter
    def colour(self, colour):
        self.__colour = colour

    @property
    def font(self):
        return self.__font

    @font.setter
    def font(self, font):
        self.__font = font

    @property
    def font_style(self):
        return self.__font_style

    @font_style.setter
    def font_style(self, font_style):
        self.__font_style = font_style
