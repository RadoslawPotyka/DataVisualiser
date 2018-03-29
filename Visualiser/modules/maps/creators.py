from abc import abstractmethod
from enum import Enum

from folium import Map, FeatureGroup, CircleMarker, LayerControl, RegularPolygonMarker, Marker

from .models import MapLayerDocument, MapDocument, MapOptions
from .errors import InvalidCoordinatesError

from ..common.creators import DocumentFactory, DocumentRecipe
from ..common.models import Layer, ObjectFigure


class MarkerRecipe(DocumentRecipe):
    """
    Recipe for basic folium Marker creation that should be appended to a folium map.
    """

    _scale = 10

    @classmethod
    def create(cls, document: MapLayerDocument, base_object: Map) -> None:
        """
        Create marker layer on a Folium Map.

        :param document: (MapLayerDocument) layer document object containing ingredients and configuration for
            creating a marker layer.
        :param base_object: (Map) Folium map to create marker on.

        :return: None
        """
        return cls._add_layer(map_object=base_object, layer_document=document)

    @classmethod
    def _add_layer(cls, map_object: Map, layer_document: MapLayerDocument) -> None:
        """
        Create layer on a Folium Map. Method creates layer and adjusts it based on configuration. The layer is
        appended to the provided Folium Map.

        :param map_object: (Map) map object to create layer on

        :param layer_document: (MapLayerDocument) layer document configuration object.

        :return: None
        """
        model = layer_document.model
        latitude_column = layer_document.latitude
        longtitude_column = layer_document.longtitude

        axis = model.axis
        axis_label = axis.name or axis.data_field
        feature_group = FeatureGroup(name=axis_label)

        data_source = layer_document.data_source
        for row in data_source.itertuples():
            latitude = getattr(row, latitude_column.data_field)
            longtitude = getattr(row, longtitude_column.data_field)
            value = getattr(row, axis.data_field)

            coordinates = [latitude, longtitude]
            # model.figure.size *= 5
            marker = cls._create_marker(layer_value=str(value), coordinates=coordinates, layer_figure=model.figure)
            feature_group.add_child(marker)

        map_object.add_child(feature_group)

    @classmethod
    @abstractmethod
    def _create_marker(cls, layer_value: str, coordinates: [float], layer_figure: ObjectFigure) -> Marker:
        """
        Create single Folium Marker object.

        :param layer_value: (str) value of layers data_field to display on markers popup.

        :param coordinates: [float] coordinates on which the marker should be displayed.

        :param layer_figure: (ObjectFigure) layer figure configuration object.

        :return: (Marker) marker instance adjusted for provided params.
        """
        return Marker(location=coordinates, popup=layer_value)


class CircleMarkerRecipe(MarkerRecipe):
    """
    Recipe for folium CircleMarker creation.
    """

    @classmethod
    def _create_marker(cls, layer_value: str, coordinates: [float], layer_figure: ObjectFigure) -> CircleMarker:
        """
        Create single Folium CircleMarker object.

        :param layer_value: (str) value of layers data_field to display on markers popup.

        :param coordinates: [float] coordinates on which the marker should be displayed

        :param layer_figure: (ObjectFigure) layer figure configuration object.

        :return: (Marker) marker instance adjusted for provided params.
        """

        return CircleMarker(location=coordinates, radius=layer_figure.size * cls._scale,
                            popup=layer_value, fill_color=layer_figure.colour, fill=True,
                            color='grey', fill_opacity=layer_figure.opacity)


class PolygonMarkerRecipe(MarkerRecipe):
    """
    Recipe for folium PolygonMarker creation.

    Attributes:
        _number_of_sides: (int) number of sides of created polygon.
    """

    _number_of_sides = 6

    @classmethod
    def _create_marker(cls, layer_value: str, coordinates: [float], layer_figure: ObjectFigure) -> CircleMarker:
        """
        Create single Folium PolygonMarker object.

        :param layer_value: (str) value of layers data_field to display on markers popup.

        :param coordinates: [float] coordinates on which the marker should be displayed

        :param layer_figure: (ObjectFigure) layer figure configuration object.

        :return: (Marker) marker instance adjusted for provided params.
        """

        return RegularPolygonMarker(location=coordinates, radius=layer_figure.size * cls._scale,
                                    popup=layer_value, fill_color=layer_figure.colour,
                                    color='grey', fill_opacity=layer_figure.opacity,
                                    number_of_sides=cls._number_of_sides)


class RectangleMarkerRecipe(PolygonMarkerRecipe):
    """
    Class representation of rectangle marker. Declares number of sides that should be used in _create method of parent
    class.
    """
    _number_of_sides = 4


class TriangleMarkerRecipe(PolygonMarkerRecipe):
    """
    Class representation of triangle marker. Declares number of sides that should be used in _create method of
    parent class.
    """
    _number_of_sides = 3


class LayerControlRecipe(DocumentRecipe):
    """
    Recipe for layer control appendage to a map.
    """

    @classmethod
    def create(cls, base_object: Map, *args, **kwargs) -> Map:
        """
        Add LayerControl feature group to provided folium map.

        :param base_object: (Map) map that layer control should be appended to.

        :return: base_object(Map) - folium map object with appended layer control.
        """
        base_object.add_child(LayerControl())

        return base_object


class MapRecipe(DocumentRecipe):
    """
    Recipe for folium Map object creation.
    """

    post_execute = LayerControlRecipe

    @classmethod
    def create(cls, document: MapDocument) -> Map:
        """
        Create Folium map to display to the user.

        :param document: (MapDocument) chart document object containing ingredients for bokeh figure creation.
        :return: plot(Map) - bokeh figure object to display to the user.
        """
        map_options = document.map_options

        map_object = cls._create_map(map_options=map_options)

        return map_object

    @classmethod
    def _create_map(cls, map_options: MapOptions) -> Map:
        """
        Creates Folium Map instance based on map configuration object.

        :param map_options: (MapOptions) Configuration object for a map.
        :return: map_object(Map) - Map object instance based on provided configuration.
        """
        map_object = Map(zoom_start=2.5, tiles=map_options.tiles, location=[40.0, 10.0])

        return map_object


class MapRecipes(Enum):
    """
    Enum class containing supported recipes for chart document factorisation.
    """
    Map = MapRecipe
    Circle = CircleMarkerRecipe
    Marker = MarkerRecipe
    RectangleMarker = RectangleMarkerRecipe
    TriangleMarker = TriangleMarkerRecipe
    Hexagon = PolygonMarkerRecipe


class MapFactory(DocumentFactory):
    """
    Map specific DocumentFactory containing all necessary methods and overridings for proper map factorisation.
    """

    def validate(self, document: MapDocument) -> None:
        super().validate(document=document)

        map_options = document.model
        data_frame = document.data_source.data
        columns = [map_options.latitude, map_options.longtitude]

        invalid_columns = self._data_frame_service.get_invalid_columns(columns_list=columns, data_frame=data_frame)

        if len(invalid_columns):
            raise InvalidCoordinatesError(coordinates=invalid_columns)

    def prepare_layer_document(self, layer: Layer, document: MapDocument) -> MapLayerDocument:
        """
        Prepares LayerDocument object for creating layer on a map.

        :param layer: (Layer) layer configuration object.
        :param document: (MapDocument) map document to append layer document to.
        :return: layer_document(MapLayerDocument) - prepared layer document to append on a map.
        """
        layer_data_source = self.prepare_layer_data_source(data_source=document.data_source,
                                                           filter_expression=layer.filter_expression)
        layer_document = MapLayerDocument(layer=layer, data_source=layer_data_source,
                                          latitude=document.model.latitude, longtitude=document.model.longtitude)
        return layer_document
