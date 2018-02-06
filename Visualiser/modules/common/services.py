from abc import abstractmethod

import os.path
from enum import Enum

import pandas as pd
from inspect import isabstract, isclass
from flask import session, redirect, render_template, url_for

from .models import User, ApplicationOptions, DataSource, FilterExpression
from .fileio import FileHandlers, FileHandler
from .utils import StringTools


class Service(object):
    """
    Base class for services. Uses class properties and methods for storing data such as running application options for
    later usage by other deriving services.

    Attributes:
        options: (ApplicationOptions) configuration options of instantiated flask application.
    """

    options = None

    @classmethod
    def set_options(cls, options: dict):
        """
        Set application config settings for all Service subclasses.

        :param options: (dict) dictionary containing configuration options for current application.
        :return: None
        """
        cls.options = ApplicationOptions(options=options)

    @classmethod
    def get_options(cls) -> ApplicationOptions:
        """
        Get configuration options for current application.

        :return: (ApplicationOptions) config options for current application.
        """
        return cls.options

    @classmethod
    def get_backend_url(cls):
        options = cls.get_options()
        return options.backend_url

    @classmethod
    def get_allowed_extensions(cls):
        options = cls.get_options()
        return options.allowed_extensions

    @classmethod
    def get_supported_colours(cls):
        options = cls.get_options()
        return options.colour_palette


class SessionService(Service):
    """
    Service handling access to session data storage.

    Attributes:
        Columns: (str) key for columns for later usage in columns select fields in document form.
    """

    Columns = "Columns"
    FileName = "FileName"

    @staticmethod
    def save_item(key: str, value: any) -> None:
        """
        Save value in the session storage by key.

        :param key: (str) key by which the value should be stored
        :param value: (str) value to save in the session storage for later usage
        :return: None
        """
        session[key] = ""
        session[key] = value

    @staticmethod
    def get_item(key: str) -> any:
        """
        Get data by provided key.

        :param key: Key by which the data is stored
        :return: Value stored under given key in session storage.
        """
        return session[key]


class WorkingContextService(Service):
    """
    Service handling, controlling and interacting with the context of the application.
    """

    @staticmethod
    def get_file_columns() -> [tuple]:
        """
        Get list of columns read from newly uploaded file to display in select fields. Returns list of two element tuple
        expected by wtforms SelectField.

        :return: [tuple] columns saved from currently uploaded file.
        """
        columns = SessionService.get_item(SessionService.Columns)
        return [(column, column) for column in columns]

    @staticmethod
    def save_file_columns(columns: [str]) -> None:
        """
        Save columns read from a file for later usage.

        :param columns: [str] list of column names to save
        :return: None
        """
        SessionService.save_item(SessionService.Columns, columns)

    @staticmethod
    def get_upload_folder() -> str:
        """
        Returns path to the folder in which uploaded files are stored. Accesses FileService and uses the file path set
        in it.

        :return upload_path: (str) path to the folder under which uploaded files are stored.
        """
        path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(path, FileService.UPLOAD_PATH)
        return upload_path

    @staticmethod
    def get_user_logged_in() -> User:
        """
        Get currently logged user. If no user is logged returns guest user.

        :return user: (User) user that is currently logged in the application
        """
        user = User(name="guest")

        return user


class FileService(Service):
    """
    Service handling upload, parsing and reading data off of a file.

    Attributes:
        UPLOAD_PATH: (str) path under which the uploaded files are stored.
        file_handlers: (FileHandlers) file handlers used for file reading.
    """

    UPLOAD_PATH = "..\\..\\..\\public\\DATA\\"
    file_handlers = FileHandlers

    @staticmethod
    def get_upload_folder() -> str:
        """
        Returns path to the folder in which uploaded files are stored.

        :return upload_path: (str) path to the folder under which uploaded files are stored.
        """
        path = os.path.abspath(os.path.dirname(__file__))
        upload_path = os.path.join(path, FileService.UPLOAD_PATH)

        return upload_path

    @staticmethod
    def read_columns(data_source: DataSource) -> [str]:
        """
        Read columns from a given file and return a list of their names.

        :param data_source: (DataSource) DataSource object instance containing options for a file.
        :return: (list(str)) list of columns names read from provided file.
        """
        file_handler = FileService.__create_file_handler(file_name=data_source.file_name)

        data_frame = file_handler.read_columns(data_source=data_source, file_path=FileService.get_upload_folder())
        DataFrameService.fix_column_names(data_frame=data_frame)

        return DataFrameService.extract_columns(data_frame=data_frame)

    @staticmethod
    def read_file(data_source: DataSource) -> pd.DataFrame:
        """
        Reads file and returns parsed pandas DataFrame object with handler of the file based on its extension.

        :param data_source: (DataSource) DataSource object instance containing options for a file.
        :return: (pd.DataFrame) pandas DataFrame object with values read and parsed from the file.
        """
        file_handler = FileService.__create_file_handler(file_name=data_source.file_name)

        data_frame = file_handler.read_file(data_source=data_source, file_path=FileService.get_upload_folder())
        DataFrameService.fix_column_names(data_frame=data_frame)

        if data_source.should_fill_missing_data:
            return DataFrameService.fill_missing_data(data_frame=data_frame)

        return data_frame

    @staticmethod
    def __get_file_type(file_name: str):
        """
        Determine and return type of the file. Method tries to fetch extension by splitting the file name by default
        returning 'csv' type.

        :param file_name: (str) name of the file to fetch extension for.
        :return extension: (str) extension of provided file_name
        """
        extension = ""

        try:
            extension = file_name.split(".")[-1]
        except IndexError:
            extension = "csv"
        finally:
            return extension

    @staticmethod
    def __create_file_handler(file_name: str) -> FileHandler:
        """
        Creates file type specific handler based on file extension provided by params (should match existing file
        handlers.

        :param file_name: (str) name of the file to prepare file handler for.
        :return: (FileHandler) file handler needed for proper parsing of the file with provided extension.
        """
        file_handler_type = FileService.__get_file_type(file_name=file_name)

        if file_handler_type not in FileService.get_allowed_extensions():
            raise TypeError("Unsupported type {0} ".format(file_handler_type))

        file_handler = FileService.file_handlers[file_handler_type].value

        if isabstract(file_handler) or not isclass(file_handler):
            raise TypeError("File handler not implemented for type {0}".format(file_handler_type))

        return file_handler()


class DataFrameService(object):
    """
    Service handling pandas DataFrame objects and performing operations on them such as interpolation used for filling
    missing data or filtering data based on condition.
    """

    @staticmethod
    def fill_missing_data(data_frame: pd.DataFrame) -> pd.DataFrame:
        """
        Fills missing data in the data_frame using interpolation method.

        :param data_frame: (pd.DataFrame) pandas DataFrame object to perform interpolation on.
        :return: (pd.DataFrame) interpolated DataFrame object with missing data filled.
        """
        return data_frame.interpolate()

    @staticmethod
    def filter(data_frame: pd.DataFrame, filter_expression: FilterExpression) -> pd.DataFrame:
        """
        Filters data in provided data_frame by provided filter_expression. Uses DataFrame query method to perform
        filtering.

        :param data_frame: (pd.DataFrame) DataFrame object to perform filtering on.
        :param filter_expression: (FilterExpression) filter expression to filter data by.
        :return df: (pd.DataFrame) DataFrame object with filtered data based on provided expression.
        """
        query = str(filter_expression)
        print(query)
        df = data_frame.query(query)
        return df

    @staticmethod
    def extract_columns(data_frame: pd.DataFrame) -> [str]:
        """
        Extract columns list from provided data frame.

        :param data_frame: (pd.DataFrame) DataFrame object instance to extract columns from.
        :return: list of columns from provided data frame.
        """
        return data_frame.columns.values.tolist()

    @staticmethod
    def fix_column_names(data_frame: pd.DataFrame) -> None:
        """
        Replaces whitespaces in provided data_frame columns with underscores to avoid errors in data_frame querying.

        :param data_frame: (pd.DataFrame) data frame to replace whitespaces for.
        :return: None
        """
        cols = data_frame.columns
        cols = cols.map(lambda x: StringTools.to_snake_case(string=x))
        data_frame.columns = cols


class DocumentService(Service):
    """
    Base interface for document service. Contains method necessary for correct work in base  context of the document.
    """

    @classmethod
    @abstractmethod
    def get_supported_shapes(cls) -> [tuple]:
        """
        Return supported shapes for a document. Returns shapes in format expected by wtforms SelectField.

        :return: ([tuple]) list of supported shapes for given document.
        """
        return None

    @classmethod
    @abstractmethod
    def get_supported_shape_keys(cls) -> Enum:
        """
        Return enum object containing shape keys supported for a given document.

        :return: (Enum) Enum object containing keys of supported objects.
        """
        return None

    @classmethod
    def get_supported_colours(cls):
        """
        Return supported colours for a document. Returns colours in format expected by wtforms SelectField.

        :return: ([tuple]) list of supported colours for given document.
        """
        colours = cls.get_options().colour_palette
        return [(colour, colour) for colour in colours]


class RouterStateService(Service):
    """
    Service handling routing, redirecting and rendering template.
    """

    @staticmethod
    def go(state: str) -> redirect:
        """
        Redirect user to a state provided with method params.

        :param state: (str) state to redirect user to. Should contain full endpoint with blueprint name for proper
        redirection between and inside blueprints.

        :return: route matching provided state.
        """
        return redirect(url_for(state))

    @staticmethod
    def submit(state: str) -> redirect:
        """
        Redirect user to a state provided with method params using request POST method.

        :param state: (str) state to redirect user to. Should contain full endpoint with blueprint name for proper
        redirection between and inside blueprints.

        :return: route matching provided state.
        """
        return redirect(url_for(state), code=307)

    @staticmethod
    def render(template_path: str, controller: any) -> render_template:
        """
        Renders view with controller.

        :param template_path: (str) path to the template that should be displayed to a user.
        :param controller: (any) controller that should be assigned to rendered template.
        :return: rendered template with bound controller.
        """
        return render_template(template_path, controller=controller)


class CommonServiceProvider(object):
    """
    Service provider for common module. Contains exportable services for later usage throughout the application.
    """
    WorkingContextService = WorkingContextService
    DocumentService = DocumentService
    FileService = FileService
    RouterStateService = RouterStateService
    DataFrameService = DataFrameService
