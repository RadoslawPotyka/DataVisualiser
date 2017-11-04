class Chart(object):
    """
    Represents chart for data visualisation. Contains useful information and data
    for chart creation and customisation.

    Attributes:
        @property id(int): chart id for identyfying particular chart
        @property width(int): width of the chart in pixels
        @property height(int): height of the chart in pixels
        @property x_axis(Axis): Axis class instance for determining values and display of X axis of the chart
        @property y_axis(Axis): Axis class instance for determining values and display of Y axis of the chart
        @property title(ChartTitle): Title class instance containing styling and display of chart title
        @property figure(Figure): Figure class instance containing options for shape to be displayed on the chart
    """

    def __init__(self):
        self.__id = None
        self.__width = None
        self.__height = None
        self.__X_axis = Axis()
        self.__Y_axis = Axis()
        self.__title = ChartTitle()
        self.__figure = Figure()

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id):
        self.__id = new_id

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

    @property
    def y_axis(self):
        return self.__Y_axis

    @property
    def title(self):
        return self.__title

    @property
    def figure(self):
        return self.__figure


class Axis(object):
    """
    Object representation of an axis containing options necessary for controlling axis on a chart.

    @property name(str): display name of an axis.
    @property data_field(str): column name used for an axis.
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


class Figure(object):
    """
    Object representation of a figure on a plot. Contains data necessary for customising point, lines and other
    geometrical shapes on a plot.

    Attributes:
        @property colour(str): Colour of the figure. Can be string description or code for a colour.
        @property opacity(str): Determines transparency of the figure.
        @property size(str): Determines width of the figure on the plot in pixels.
    """

    def __init__(self):
        self.__colour = None
        self.__opacity = None
        self.__size = None

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
