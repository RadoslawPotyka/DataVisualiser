from abc import abstractmethod
from enum import Enum

from Folium import Map, FeatureGroup, CircleMarker, LayerControl, Marker

from .models import MapLayerDocument, MapDocument, MapOptions
from ..common.creators import DocumentFactory, DocumentRecipe
from ..common.models import Layer, ObjectFigure


class MarkerRecipe(DocumentRecipe):
    @classmethod
    def create(cls, document: Map, base_object: MapLayerDocument) -> None:
        """
        Create marker layer on a Folium Map.

        :param document: (MapLayerDocument) layer document object containing ingredients and configuration for
        creating a marker layer.
        :param base_object: (Map) Folium map to create marker on
        :return: None
        """
        return cls._add_layer(map_object=document, layer_document=base_object)

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
            marker = cls._create_marker(layer_value=str(value), coordinates=coordinates, layer_figure=model.figure)

            feature_group.add_child(marker)

        map_object.add_child(feature_group)

    @classmethod
    @abstractmethod
    def _create_marker(cls, layer_value: str, coordinates: [float], layer_figure: ObjectFigure) -> Marker:
        """
        Create single Folium Marker object.

        :param layer_value: (str) value of layers data_field to display on markers popup.
        :param coordinates: [float] coordinates on which the marker should be displayed
        :param layer_figure: (ObjectFigure) layer figure configuration object.
        :return: (Marker) marker instance adjusted for provided params.
        """
        return Marker(location=coordinates, popup=layer_value)


class CircleMarkerRecipe(MarkerRecipe):
    @classmethod
    def _create_marker(cls, layer_value: str, coordinates: [float], layer_figure: ObjectFigure) -> CircleMarker:
        """
        Create single Folium CircleMarker object.

        :param layer_value: (str) value of layers data_field to display on markers popup.
        :param coordinates: [float] coordinates on which the marker should be displayed
        :param layer_figure: (ObjectFigure) layer figure configuration object.
        :return: (Marker) marker instance adjusted for provided params.
        """

        return CircleMarker(location=coordinates, radius=layer_figure.size,
                            popup=layer_value, fill_color=layer_figure.colour, fill=True,
                            color='grey', fill_opacity=layer_figure.opacity)


class MapRecipe(DocumentRecipe):
    @classmethod
    def create(cls, document: MapDocument) -> Map:
        """
        Create Folium map to display to the user.

        :param document: (MapDocument) chart document object containing ingredients for bokeh figure creation.
        :return plot: (Map) bokeh figure object to display to the user.
        """
        map_options = document.map_options

        map_object = cls._create_map(map_options=map_options)

        return map_object

    @classmethod
    def _create_map(cls, map_options: MapOptions) -> Map:
        """
        Creates Folium Map instance based on map configuration object.

        :param map_options: (MapOptions) Configuration object for a map.
        :return map_object: (Map) Map object instance based on provided configuration.
        """
        map_object = Map(zoom_start=6, world_copy_jump=True, tiles=map_options.tiles,
                         height=map_options.height, width=map_options.width)
        map_object.add_child(LayerControl())

        return map_object


class MapRecipes(Enum):
    """
    Enum class containing supported recipes for chart document factorisation.
    """
    Map = MapRecipe
    Circle = CircleMarkerRecipe
    Marker = MarkerRecipe


class MapFactory(DocumentFactory):
    def prepare_layer_document(self, layer: Layer, document: MapDocument) -> MapLayerDocument:
        """
        Prepares LayerDocument object for creating layer on a map.

        :param layer: (Layer) layer configuration object.
        :param document: (MapDocument) map document to append layer document to.
        :return layer_document: (MapLayerDocument) prepared layer document to append on a map.
        """
        layer_data_source = self.prepare_layer_data_source(data_source=document.data_source,
                                                           filter_expression=layer.filter_expression)

        layer_document = MapLayerDocument(layer=layer, data_source=layer_data_source,
                                          latitude=document.model.latitude, longtitude=document.model.longtitude)
        return layer_document
