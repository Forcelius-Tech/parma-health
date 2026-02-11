from abc import ABC, abstractmethod
from typing import Generator
import pandas as pd
import os


class DataConnector(ABC):
    """
    Abstract base class for all data connectors in the Parma Health Toolkit.
    Connectors are responsible for reading from and writing to data sources.
    """

    @abstractmethod
    def read(self) -> Generator[pd.DataFrame, None, None]:
        """
        Reads data from the configured source.
        MUST yield data in chunks (pandas DataFrames) to handle large datasets.
        """
        pass

    @abstractmethod
    def write(self, data: Generator[pd.DataFrame, None, None]) -> None:
        """
        Writes data to the configured destination.
        Accepts a generator of pandas DataFrames.
        """
        pass


class CSVConnector(DataConnector):
    """
    Connector for reading and writing CSV files.
    Supports chunked reading and writing to handle large files.
    """
    def __init__(self, path: str, chunksize: int = 1000):
        self.path = path
        self.chunksize = chunksize

    def read(self) -> Generator[pd.DataFrame, None, None]:
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"File not found: {self.path}")

        # type: ignore[call-overload]
        with pd.read_csv(self.path, chunksize=self.chunksize) as reader:
            yield from reader

    def write(self, data: Generator[pd.DataFrame, None, None]) -> None:
        first_chunk = True
        # Ensure directory exists
        os.makedirs(os.path.dirname(os.path.abspath(self.path)), exist_ok=True)

        for chunk in data:
            mode = 'w' if first_chunk else 'a'
            header = first_chunk
            chunk.to_csv(self.path, mode=mode, header=header, index=False)  # type: ignore[call-overload]  # noqa: E501
            first_chunk = False
