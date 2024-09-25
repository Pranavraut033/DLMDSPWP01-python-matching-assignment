import pandas as pd


class DataFormatError(Exception):
    pass


class FileHandler:
    """
    FileHandler is a class responsible for handling file operations, specifically loading data from a CSV file.

    Attributes:
        file_path (str): The path to the CSV file.
        data (pd.DataFrame): The data loaded from the CSV file.

    Methods:
        __init__(file_path: str):
            Initializes the FileHandler with the given file path and loads the data.

        load_data() -> pd.DataFrame:
            Loads data from the CSV file specified by file_path.
            Returns:
                pd.DataFrame: The data loaded from the CSV file.
            Raises:
                DataFormatError: If there is an error loading the data from the file.
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
