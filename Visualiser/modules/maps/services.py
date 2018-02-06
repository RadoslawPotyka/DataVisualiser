from enum import Enum

from Folium import Map

from .creators import MapRecipes, MapFactory
from .models import MapDocument

from ..common.services import CommonServiceProvider


class MapService(CommonServiceProvider.DocumentService):
    """
    Service containing common methods for handling maps and objects and operations related to them.
    """

    __supported_tiles = ["Stamen Tone", "Stamen Terrain", "Mapbox Bright",
                         "openstreetmap", "MapQuest Open Aerial", "stamenwatercolor"]

    @staticmethod
    def get_supported_recipes() -> MapRecipes:
        return MapRecipes

    @staticmethod
    def get_recipe(recipe_name: str) -> Enum:
        return MapRecipes[recipe_name]

    @classmethod
    def get_supported_shapes(cls) -> [str]:
        shapes = [(key.name, key.name) for key in MapRecipes if key != MapRecipes.Map]
        return shapes

    @classmethod
    def get_supported_shape_keys(cls) -> [str]:
        super().get_supported_shape_keys()
        return MapService.get_supported_recipes()

    @staticmethod
    def get_supported_tiles() -> [tuple]:
        supported_tiles = MapService.__supported_tiles
        return [(tile, tile) for tile in supported_tiles]


class FoliumService(object):
    """
    Static service handling Folium map generation and export.
    """

    __default_map_name = "map.html"

    @staticmethod
    def generate_plot(map_document: MapDocument) -> Map:
        """
        Generate plot for given pandas DataFrame and chart options. Returns created map object

        :param map_document: (MapDocument) options for a map containing its configuration object and data source.
        :return generated_map: (Map) bokeh plot object
        """
        factory = MapFactory(recipes=MapService.get_supported_recipes(),
                             data_frame_service=CommonServiceProvider.DataFrameService)
        generated_map = factory.create_object(document=map_document)

        return generated_map

    @staticmethod
    def export_map(map_object: Map) -> None:
        """
        Export map as html file.

        :param map_object: (Map) bokeh figure object to export resources from.
        :return: None.
        """
        upload_path = CommonServiceProvider.FileService.get_upload_folder()
        file_name = FoliumService.__default_map_name
        full_name = upload_path + "/{0}".format(file_name)

        map_object.save(full_name)
