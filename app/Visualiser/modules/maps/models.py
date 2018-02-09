import pandas as pd

from ..common.models import DocumentOptions, LayerDocument, Axis, Layer, Document, ObjectKey


class MapLayerDocument(LayerDocument):
    """
    Represents chart configuration for data visualisation. Contains useful information and data
    for chart creation and customisation.

    Attributes:
        @property latitude(Axis): Axis class instance for determining values for latitudes of a map.
        @property longtitude(Axis): Axis class instance for determining values for longtitudes of a map.
    """
    def __init__(self,
                 layer: Layer = None,
                 data_source: pd.DataFrame = None,
                 latitude: Axis = Axis(),
                 longtitude: Axis = Axis()):
        super().__init__(layer=layer, data_source=data_source)
        self.__latitude = latitude
        self.__longtitude = longtitude

    @property
    def latitude(self) -> Axis:
        return self.__latitude

    @latitude.setter
    def latitude(self, latitude_column: Axis) -> None:
        self.__latitude = latitude_column

    @property
    def longtitude(self) -> Axis:
        return self.__longtitude

    @longtitude.setter
    def longtitude(self, longtitude_column: Axis) -> None:
        self.__longtitude = longtitude_column


class MapOptions(DocumentOptions):
    """
    Represents chart configuration for data visualisation. Contains useful information and data
    for chart creation and customisation.

    Attributes:
        @property latitude(Axis): Axis class instance for determining values for latitudes of a map.
        @property longtitude(Axis): Axis class instance for determining values for longtitudes of a map.
    """

    def __init__(self):
        super().__init__()
        self.__latitude = Axis()
        self.__longtitude = Axis()
        self.__tiles = None

    @property
    def latitude(self) -> Axis:
        return self.__latitude

    @latitude.setter
    def latitude(self, latitude_column: Axis) -> None:
        self.__latitude = latitude_column

    @property
    def longtitude(self) -> Axis:
        return self.__longtitude

    @longtitude.setter
    def longtitude(self, longtitude_column: Axis) -> None:
        self.__longtitude = longtitude_column

    @property
    def tiles(self) -> str:
        return self.__tiles

    @tiles.setter
    def tiles(self, tiles: str) -> None:
        self.__tiles = tiles


class MapDocument(Document):
    """
    Represents whole chart object ready to display. Wraps chart configuration and its data source for easier
    transportation throughout solution and its services.

    Attributes:
        @property chart_options(ChartOptions): chart configuration object for the chart.
        @property data_source(pandas.DataFrame): data source used in the chart.
    """

    _object_key = ObjectKey.Map

    def __init__(self):
        super().__init__()

    @property
    def map_options(self) -> MapOptions:
        return self._model

    @map_options.setter
    def map_options(self, map_options: MapOptions):
        self._model = map_options

    @property
    def model(self) -> MapOptions:
        return self._model

    @model.setter
    def model(self, map_options: MapOptions):
        self._model = map_options
