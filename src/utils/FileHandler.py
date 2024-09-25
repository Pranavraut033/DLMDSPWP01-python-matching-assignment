import pandas as pd


class DataFormatError(Exception):
    pass


class FileHandler:
    """
    FileHandler is a class for handling file operations, specifically loading data from a CSV file.

    Attributes:
        file_path (str): The path to the CSV file.
        data (pd.DataFrame): The data loaded from the CSV file.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data = self.load_data()

    def load_data(self) -> pd.DataFrame:
        try:
            data = pd.read_csv(self.file_path)
            return data
        except Exception as e:
            raise DataFormatError(f"Error loading data from {self.file_path}: {e}")
