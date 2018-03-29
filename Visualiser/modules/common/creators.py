import pandas as pd

from abc import abstractmethod
from enum import Enum

from .utils import Factory, Recipe
from .models import Document, LayerDocument, Layer, FilterExpression, DataSource
from .services import CommonServiceProvider


"""
.. module:: creators
   :synopsis: Common and base models for utilities usage in the application.

"""


class DocumentRecipe(Recipe):
    """
    Interface for document recipes functionality asserting that all recipe command classes will have respective create
    methods.
    """

    @classmethod
    @abstractmethod
    def create(cls, *args, **kwargs) -> any:
        """
        Create object and return its instance.

        :return: (any) any object
        """
        pass

    @classmethod
    def execute(cls, document: Document = None, base_object: any = None) -> object:
        """
        Executes document recipe command by returning call to create method from called class.

        :param document: (Document) document containing ingredients for executing the command
        :param base_object: (any) optional param for recipe execution. Provide this param when recipe appends object to
            another one rather then creating a new one.
        :return: (object) result of create method from provided subclass.
        """
        if base_object is None:
            return cls.create(document=document)
        else:
            return cls.create(document=document, base_object=base_object)


class DocumentFactory(Factory):
    """
    Interface for Document factorisation. Contains methods necessary for proper handling of all documents factorisation.

    Attributes:
        _recipes: (Enum) enumerator object containing recipes for document factory.

        _data_frame_service: (CommonServiceProvider.DataFrameService) Service for handling with the data frame objects.

        _post_creation_tasks: (list) tasks to perform after the document is created.

    Args:
        recipes: (Enum) enumerator object containing recipes for document factory.

        data_frame_service: (CommonServiceProvider.DataFrameService) Service for handling with the data frame objects.
    """

    def __init__(self,
                 recipes: Enum,
                 data_frame_service: CommonServiceProvider.DataFrameService = CommonServiceProvider.DataFrameService):
        self._recipes = recipes
        self._data_frame_service = data_frame_service
        self._post_creation_tasks = []

    def create_object(self, document: Document) -> any:
        """
        Method builds base document and then appends to it each layer of provided documents model and returns it.

        :param document: (Document) characteristics and ingredients necessary for proper creation of the object.
        :return: created_object(any) - instance of an object created from ingredients provided in params.
        """
        self.validate(document=document)

        created_object = self.build(document=document)

        for layer in document.model.layers:
            layer_document = self.prepare_layer_document(layer=layer, document=document)
            self.build(base_object=created_object, document=layer_document)

        return self.__post_create(document=document, base_object=created_object)

    def __post_create(self, document: Document = None, base_object: any = None) -> any:
        """
        Run all recipes that should be executed after document creation.

        :param document: (Document) characteristics and ingredients necessary for proper creation of the object.
        :param base_object: (any) optional param for recipe execution. Provide this param when recipe appends object to
            another one rather then creating a new one.
        :return: base_object(any) - object created by factory with all modifications related to post creation tasks.
        """
        for additional_task in self._post_creation_tasks:
            additional_task.execute(document=document, base_object=base_object)

        return base_object

    @abstractmethod
    def prepare_layer_document(self, layer: Layer, document: Document) -> LayerDocument:
        """
        Prepares LayerDocument object for creating layer on a document.

        :param layer: (Layer) layer configuration object.
        :param document: (Document) document to append LayerDocument to.
        :return: layer_document(LayerDocument) - prepared layer document to append on a document.
        """
        pass

    def prepare_layer_data_source(self, data_source: DataSource,
                                  filter_expression: FilterExpression = None) -> pd.DataFrame:
        """
        Prepare data source for layer filtering the data if filter_expression is provided.

        :param data_source: (DataSource) base data source object to assign to layer document.
        :param filter_expression: (FilterExpression) filter expression to filter data by before assigning to layer
            document.
        :return: layer_data_source(pd.DataFrame) - prepared and filtered data_source for a layer.
        """
        data_frame = data_source.data

        if filter_expression is not None:
            layer_data_source = self._data_frame_service.filter(data_frame=data_frame,
                                                                filter_expression=filter_expression)
        else:
            layer_data_source = data_frame

        return layer_data_source

    def build(self, document: Document, base_object: any = None) -> any:
        """
        Build object from document data. Method finds recipe by object_key of the document executes it and returns
        result of the recipe execution.

        :param document: (Document) ingredients and characteristics of object to create.
        :param base_object: (any) optional param for recipe execution. Provide this param when recipe appends object to
            another one rather then creating a new one.
        :return: instance (any) object created by recipe execution.
        """
        recipe = self._get_recipe(object_key=document.object_key)

        instance = recipe.execute(document=document, base_object=base_object)

        if recipe.post_execute is not None:
            self._post_creation_tasks.append(recipe.post_execute)

        return instance

    @abstractmethod
    def validate(self, document: Document) -> None:
        """
        Validates data in document. Should raise an error if data in provided document is incorrect.

        :return: None
        """
        pass
