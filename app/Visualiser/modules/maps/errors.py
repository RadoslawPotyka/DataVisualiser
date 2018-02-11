from ..common.errors import CreatorError
from ..common.utils import StringTools


class InvalidCoordinatesError(CreatorError):
    _error = "Some of the coordinates you provided are not numbers: {invalid_columns}."
    _document_type = "Map"
    _invalid_columns = []

    def __init__(self, coordinates: [str]):
        self._invalid_columns = coordinates
        error_message = StringTools.parse_params(self._error, self.__params)

        super().__init__(document_type=self._document_type, error=error_message)

    @property
    def __params(self):
        return {
            "invalid_columns": self._invalid_columns,
            "document": self._document_type,
        }
