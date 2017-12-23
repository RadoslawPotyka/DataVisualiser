from abc import abstractmethod, ABCMeta
from enum import Enum


class Recipe(metaclass=ABCMeta):
    """
    Base interface for function objects.
    """

    @classmethod
    @abstractmethod
    def execute(cls, *args, **kwargs):
        pass


class Factory(metaclass=ABCMeta):
    """
    Interface for factorisation.

    Attributes:
        _recipes: (Enum) recipes enumerator containing keys and corresponding recipe function object.
    """

    _recipes = None

    def _get_recipe(self, object_key: Enum) -> Recipe:
        """
        Get recipe function object by object_key.

        :param object_key: (Enum) key of the object to fetch recipe for
        :return recipe: (Recipe) recipe for object with provided key
        """
        recipe = self._recipes[object_key.name].value

        if recipe is None:
            # TODO: extract to decorator
            raise AttributeError("Unknown recipe!")

        return recipe

    @abstractmethod
    def build(self, *args, **kwargs) -> any:
        pass
