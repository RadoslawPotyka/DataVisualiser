from enum import Enum
import pandas as pd


class ObjectKey(Enum):
    """
    Enumerator subclass containing keys for objects used in application.
    """
    Chart = "Chart"
    Map = "Map"
    Line = "Line"
    Square = "Square"
    Triangle = "Triangle"
    Circle = "Circle"


class ObjectFigure(object):
    """
    Object representation of a object_key. Contains data necessary for customising point, lines and other
    geometrical shapes on a plot or map.

    Attributes:
        @property object_key(Enum): Object key of the layer representing it's shape.
        @property colour(str): Colour of the figure. Can be string description or code for a colour.
        @property opacity(str): Determines transparency of the figure.
        @property size(str): Determines width of the figure on the plot in pixels.
    """

    def __init__(self):
        self.__object_key = None
        self.__colour = None
        self.__opacity = None
        self.__size = None

    @property
    def object_key(self) -> ObjectKey:
        return self.__object_key

    @object_key.setter
    def object_key(self, shape: ObjectKey):
        self.__object_key = shape

    @property
    def colour(self):
        return self.__colour

    @colour.setter
    def colour(self, colour: str):
        self.__colour = colour

    @property
    def opacity(self):
        return self.__opacity

    @opacity.setter
    def opacity(self, opacity: float):
        self.__opacity = opacity

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size: int):
        self.__size = size


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
    def name(self, name: str):
        self.__name = name

    @property
    def data_field(self):
        return self.__data_field

    @data_field.setter
    def data_field(self, data_field: str):
        self.__data_field = data_field

    @property
    def data_type(self):
        return self.__data_type

    @data_type.setter
    def data_type(self, data_type: str):
        self.__data_type = data_type


class Layer(object):
    """
    Object representation of a chart layer covering the Y axis settings and figure to display.

    Attributes:
        @property axis(Axis): Axis class instance for determining values and display of Y axis of the chart layer.
        @property figure(ChartFigure): ChartFigure class instance containing options for object_key to be displayed on the
        chart layer.
    """

    def __init__(self):
        self.__axis = None
        self.__figure = None

    @property
    def axis(self) -> Axis:
        return self.__axis

    @property
    def figure(self) -> ObjectFigure:
        return self.__figure

    @axis.setter
    def axis(self, axis: Axis):
        self.__axis = axis

    @figure.setter
    def figure(self, figure: ObjectFigure):
        self.__figure = figure


class DocumentOptions(object):
    """
    Represents document configuration. Contains useful information and data
    for chart creation and customisation.

    Attributes:
        @property description(str): description of the chart
        @property layers(list(ChartFigure)): List of all layers to be displayed on chart.
    """

    def __init__(self):
        self.__description = None
        self.__X_axis = Axis()
        self.__layers = []

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, name: str):
        self.__description = name

    @property
    def x_axis(self) -> Axis:
        return self.__X_axis

    @x_axis.setter
    def x_axis(self, axis: Axis):
        self.__X_axis = axis

    @property
    def layers(self) -> [Layer]:
        return self.__layers

    @layers.setter
    def layers(self, layers: [Layer]):
        self.__layers = layers


class Document(object):
    """
    Object representation of a document containing it's fields and object key alongside the data_source against which
    it should be bound.

    Attributes:
        @property model(DocumentOptions): model object containing characteristics of the document.
        @property data_source(pd.DataFrame): data source object for document.
        @property object_key(Enum): object key of the document.
    """

    _model = None
    _data_source = None
    _object_key = None

    @property
    def model(self) -> DocumentOptions:
        return self._model

    @property
    def data_source(self) -> pd.DataFrame:
        return self._data_source

    @data_source.setter
    def data_source(self, data_source: pd.DataFrame):
        self._data_source = data_source

    @property
    def object_key(self) -> ObjectKey:
        return self._object_key


class LayerDocument(Document):
    """
    Object representation of layer document. Translates configuration of a layer to document structure.

    Attributes:
        @property model(Layer): model object containing characteristics of a layer.
        @property data_source(pd.DataFrame): data source object for the layer.
        @property object_key(Enum): object key of the layer.
        @property x_axis(Axis): x_axis used for the layer.
    """
    def __init__(self,
                 layer: Layer = None,
                 data_source: pd.DataFrame = None,
                 x_axis: Axis = None):
        self._model = layer
        self._data_source = data_source
        self._object_key = layer.figure.object_key
        self.__X_axis = x_axis
        print(layer.figure)

    @property
    def model(self) -> Layer:
        return self._model

    @property
    def x_axis(self) -> Axis:
        return self.__X_axis

    @x_axis.setter
    def x_axis(self, axis: Axis):
        self.__X_axis = axis


class FormState(Enum):
    """
    Class enumerating possible states for a form.

    Attributes:
        BASE: represents state when form is handling base data for an object.
        LAYER: represents state when form is handling layers of an object (used only for documents)
        SUBMIT: represents state when form is valid and ready for submission.
    """
    BASE = 0
    LAYER = 1
    SUBMIT = 2


class TemplateResourcesData(object):
    """
    Object representation of template metadata for inclusion in the template file. Contains lists of html, css and html
    strings which can be embedded in a template file embedding.

    Attributes:
        @property css(str): list of string containing links to css stylesheets.
        @property js(str): list of strings containing script to include in a html page.
        @property html(str): list of stringified html files to include in an html page.
    """

    def __init__(self):
        self.__css = None
        self.__js = None
        self.__html = None

    @property
    def css(self):
        return self.__css

    @css.setter
    def css(self, css):
        self.__css = css

    @property
    def js(self):
        return self.__js

    @js.setter
    def js(self, js):
        self.__js = js

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, html):
        self.__html = html


class User(object):
    def __init__(self, name=None, login=None):
        self.__name = name
        self.__login = login

    @property
    def name(self):
        return self.__name

    @property
    def login(self):
        return self.__login
