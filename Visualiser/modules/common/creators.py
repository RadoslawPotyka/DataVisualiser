from abc import abstractmethod
from enum import Enum

from .utils import Factory, Recipe
from .models import Document, LayerDocument


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
    """

    def __init__(self, recipes: Enum):
        self._recipes = recipes

    def create_object(self, document: Document) -> any:
        """
        Method builds base document and then appends to it each layer of provided documents model and returns it.

        :param document: (Document) characteristics and ingredients necessary for proper creation of the object.
        :return created_object: (any) instance of an object created from ingredients provided in params.
        """
        created_object = self.build(document=document)

        for layer in document.model.layers:
            self.build(base_object=created_object, document=LayerDocument(layer=layer,
                                                                          data_source=document.data_source,
                                                                          x_axis=document.model.x_axis))
        return created_object

    def build(self, document: Document, base_object: any = None) -> any:
        """
        Build object from document data. Method finds recipe by object_key of the document executes it and returns
        result of the recipe execution.

        :param document: (Document) ingredients and characteristics of object to create.
        :param base_object: (any) optional param for recipe execution. Provide this param when recipe appends object to
        another one rather then creating a new one.
        :return instance: (any) object created by recipe execution.
        """
        recipe = self._get_recipe(object_key=document.object_key)
        instance = recipe.execute(document=document, base_object=base_object)

        return instance
