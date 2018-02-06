from abc import abstractmethod, ABCMeta
from enum import Enum

from numpy import unicode


class Recipe(metaclass=ABCMeta):
    """
    Base interface for function objects.
    """

    @classmethod
    @abstractmethod
    def execute(cls, *args, **kwargs) -> any:
        """
        Executes command.

        :param args: arguments used for command execution.
        :param kwargs: keyword arguments used for command execution
        :return: (any) value returned by command execution.
        """
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
        """
        Build object.

        :param args: arguments used for object creation.
        :param kwargs: keyword arguments used for object creation
        :return: (any) value returned by object creation.
        """
        pass


class StringTools(object):
    """
    Tools object containing functional tools for working and interacting with string objects.
    """
    @staticmethod
    def to_float(string: str) -> float:
        """
        Parse string to a float value.

        :param string: (str) string to parse onto a float object.
        :return: (float) float value parsed from provided string.
        """
        return float(string.replace(",", "."))

    @staticmethod
    def is_empty(string: str) -> bool:
        """
        Check whether the provided string is empty or is None object.

        :param string: (str) string to check.
        :return: (bool) boolean value determining provided string emptiness.
        """
        return string == "" or string is None

    @staticmethod
    def parse(string: str) -> any:
        """
        Guess the data type written in string and return its instance.

        :param string: (str) string to extract data from.
        :return: (any) parsed value from string.
        """
        try:
            return StringTools.to_float(string)
        except ValueError:
            return "'{0}'".format(string)

    @staticmethod
    def to_snake_case(string: str) -> str:
        """
        Return string in snake_case by replacing spaces in it with underscores.

        :param string: (str) string to replaces spaces for.
        :return: (str) string with spaces replaced by underscores.
        """
        return string.replace(' ', '_') if isinstance(string, (str, unicode)) else string
