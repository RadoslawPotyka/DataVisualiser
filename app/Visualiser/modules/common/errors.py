from .utils import StringTools


class VisualiserError(Exception):
    """
    Base class for application errors. Parses error and solution provided in derived VisualiserError sub-class.

    Args:
        solution: (str) recommended solution for the error.
        error: (str) message describing cause of the error.

    Attributes:
        @property __params: (dict) dictionary with errors string param keys and their respective values.
        @property error: (str) message of thrown error.
        @property solution: (str) solution message of thrown error.
    """
    _message = "{error}\n" \
               "{solution}"
    __error = ''
    __solution = ''

    def __init__(self, solution: str = None, error: str = None):
        self.__error = error
        self.__solution = solution

        message = StringTools.parse_params(string=self._message, params=self.__params)
        super().__init__(message)

    @property
    def error(self):
        return self.__error

    @property
    def solution(self):
        return self.__solution

    @property
    def __params(self):
        return {
            "error": self.__error,
            "solution": self.__solution
        }


class UnhandledError(VisualiserError):
    _error = "Unhandled error occurred"
    _solution = ":("

    def __init__(self):
        super().__init__(solution=self._solution, error=self._error)

    @property
    def __params(self):
        return {}


class UnsupportedExtensionError(VisualiserError):
    _error = "Unsupported file extension - {extension}"
    _solution = "Supported extensions are {supported_extensions}"

    _extension = ""
    _supported_extensions = ""

    def __init__(self, extension, supported_extensions):
        self._extension = extension
        self._supported_extensions = supported_extensions

        error = StringTools.parse_params(params=self.__params, string=self._error)
        solution = StringTools.parse_params(params=self.__params, string=self._solution)

        super().__init__(error=error, solution=solution)

    @property
    def __params(self):
        return {
            "extension": self._extension,
            "supported_extensions": self._supported_extensions
        }


class IncorrectFileNameError(VisualiserError):
    _error = "File name of uploaded file - {file_name} is incorrect"
    _solution = "Please check the name of your file"

    def __init__(self, file_name: str = ""):
        self._file_name = file_name

        error = StringTools.parse_params(string=self._error, params=self.__params)
        super().__init__(error=error, solution=self._solution)

    @property
    def __params(self):
        return {
            "file_name": self._file_name
        }


class ParsingError(VisualiserError):
    _error = "The file you've provided cannot be passed."
    _solution = "Please check if you've chosen the correct columns, their separator and their index."

    def __init__(self, error: str = None, solution: str = None):
        if error is not None:
            self._error = error

        if solution is not None:
            self._solution = solution

        super().__init__(error=self._error, solution=self._solution)


class CreatorError(VisualiserError):
    _error_message = "{document} could not be created - {error}"
    _solution_message = "Please check if data you provided is correct."

    def __init__(self, error, solution: str = None, document_type: str = "Document"):
        self._error = error
        self._document_type = document_type

        if solution is not None:
            self._solution_message = solution

        error_message = StringTools.parse_params(string=self._error_message, params=self.__params)
        super().__init__(solution=self._solution_message, error=error_message)

    @property
    def __params(self):
        return {
            "error": self._error,
            "document": self._document_type
        }
