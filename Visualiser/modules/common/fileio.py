import pandas as pd

from abc import ABCMeta, abstractmethod
from enum import Enum

from .models import DataSource


class FileHandler(metaclass=ABCMeta):
    """
    Base interface for file handlers. Allows for parsing file and reading columns from them.
    """

    @abstractmethod
    def read_file(self, data_source: DataSource, file_path: str) -> pd.DataFrame:
        """
        Read data from a file and return pandas DataFrame object instance with parsed values.

        :param data_source: (DataSource) DataSource object instance containing options for a file to read data from.
        :param file_path: (str) Path to a file to read data from
        :return: (pd.DataFrame) pandas DataFrame object instance with values parsed from a file.
        """
        pass

    @abstractmethod
    def read_columns(self, data_source: DataSource, file_path: str) -> [str]:
        """
        Read columns from a file and return list of those columns.

        :param data_source: (DataSource) DataSource object instance containing options for a file to columns data from.
        :param file_path: (pd.DataFrame) pandas DataFrame object instance with columns parsed from a file.
        :return: [str] list of columns from a file.
        """
        pass


class JSON(FileHandler):
    """
    FileHandler object for reading json type files.
    """

    def read_columns(self, data_source: DataSource, file_path: str) -> [str]:
        super().read_columns(data_source, file_path)
        data_frame = self.read_file(data_source=data_source, file_path=file_path)

        return data_frame

    def read_file(self, data_source: DataSource, file_path: str) -> pd.DataFrame:
        super().read_file(data_source, file_path)

        name = file_path + data_source.file_name
        data_frame = pd.read_json(name,
                                  typ='frame',
                                  convert_dates=data_source.datetime_columns)
        return data_frame


class CSV(FileHandler):
    """
    FileHandler object for reading csv type files.
    """

    def read_file(self, data_source: DataSource, file_path: str) -> pd.DataFrame:
        super().read_file(data_source=data_source, file_path=file_path)
        name = file_path + data_source.file_name

        df = pd.read_csv(name,
                         skiprows=data_source.column_index,
                         sep=data_source.separator,
                         parse_dates=data_source.datetime_columns)

        return df

    def read_columns(self, data_source: DataSource, file_path: str) -> [str]:
        super().read_columns(data_source=data_source, file_path=file_path)
        name = file_path + data_source.file_name

        data_frame = pd.read_csv(name,
                                 skiprows=data_source.column_index,
                                 sep=data_source.separator,
                                 nrows=1)
        return data_frame


class FileHandlers(Enum):
    """
    Enum class containing supported FileHandlers.
    """
    csv = CSV
    txt = CSV
    dat = CSV
    json = JSON
