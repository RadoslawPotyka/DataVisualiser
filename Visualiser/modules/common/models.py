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


class FormAction(Enum):
    Initialised = 0
    FileUploaded = 1
    LayerSubmitted = 2
    LayerRemoved = 3
    FormSubmitted = 4
    DocumentCreated = 5
    DocumentSaved = 6
    DocumentDisposed = 7
    DocumentEdited = 8


class DataSource(object):
    """
    Object representation of document data source.

    Attributes:
        @property data: (pd.DataFrame) DataFrame object containing data for the document.
        @property column_index: (int) Row index of columns in the DataFrame.
        @property separator: (str) Separator of columns in a file containing DataSource.
        @property file_name: (str) Name of the file containing data for the DataSource.
        @property datetime_columns: [str] List of columns with values in a datetime format.
    """

    def __init__(self):
        self.__data = None
        self.__column_index = None
        self.__separator = None
        self.__file_name = None
        self.__datetime_columns = None

    @property
    def data(self) -> pd.DataFrame:
        return self.__data

    @data.setter
    def data(self, data_frame: pd.DataFrame) -> None:
        self.__data = data_frame

    @property
    def column_index(self) -> int:
        return self.__column_index

    @column_index.setter
    def column_index(self, index: int) -> None:
        self.__column_index = index

    @property
    def separator(self) -> str:
        return self.__separator

    @separator.setter
    def separator(self, sep: str) -> None:
        self.__separator = sep

    @property
    def file_name(self) -> str:
        return self.__file_name

    @file_name.setter
    def file_name(self, file_name: str) -> None:
        self.__file_name = file_name

    @property
    def datetime_columns(self) -> [str]:
        return self.__datetime_columns

    @datetime_columns.setter
    def datetime_columns(self, datetime_columns: [str]) -> None:
        self.__datetime_columns = datetime_columns


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
        @property figure(ChartFigure): ChartFigure class instance containing options for object_key to be displayed on
        the chart layer.
    """

    def __init__(self):
        self.__axis = Axis()
        self.__figure = ObjectFigure()

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
        @property layers(list(Layer)): List of all layers to be displayed on chart.
    """

    def __init__(self):
        self.__title = None
        self.__description = None
        self.__X_axis = Axis()
        self.__layers = []

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, name: str):
        self.__title = name

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
        @property data_source(DataSource): data source object for document.
        @property object_key(Enum): object key of the document.
    """

    _model = None
    _data_source = DataSource()
    _object_key = None

    @property
    def model(self) -> DocumentOptions:
        return self._model

    @model.setter
    def model(self, new_model: DocumentOptions) -> None:
        self._model = new_model

    @property
    def data_source(self) -> DataSource:
        return self._data_source

    @data_source.setter
    def data_source(self, data_source: DataSource):
        self._data_source = data_source

    @property
    def object_key(self) -> ObjectKey:
        return self._object_key


class LayerDocument(Document):
    """
    Object representation of layer document. Translates configuration of a layer to document structure.

    Attributes:
        @property model(Layer): model object containing characteristics of a layer.
        @property data_source(pd.DataFrame): DataFrame object with values used by layer.
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

    @property
    def model(self) -> Layer:
        return self._model

    @property
    def x_axis(self) -> Axis:
        return self.__X_axis

    @x_axis.setter
    def x_axis(self, axis: Axis):
        self.__X_axis = axis

    @property
    def data_source(self) -> pd.DataFrame:
        return self._data_source

    @data_source.setter
    def data_source(self, data_source: pd.DataFrame):
        self._data_source = data_source


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


class ApplicationOptions(object):
    """
    Object representation of configuration options for running flask application.

    Attributes:
        @property backend_url: (str) url used for backend connection.
        @property colour_palette: ([str]) Colour palette supported throughout application.
        @property allowed_extensions: ([str]) file extensions supported throughout application.
    """

    __backend_url = None
    __colour_palette = None
    __allowed_extensions = None
    __environment = None

    def __init__(self, options: dict):
        self.__backend_url = options['BACKEND_URL']
        self.__colour_palette = options['COLOURS']
        self.__allowed_extensions = options['ALLOWED_EXTENSIONS']

    @property
    def backend_url(self):
        return self.__backend_url

    @property
    def colour_palette(self):
        return self.__colour_palette

    @property
    def allowed_extensions(self):
        return self.__allowed_extensions


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
