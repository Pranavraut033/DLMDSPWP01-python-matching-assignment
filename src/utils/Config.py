from dataclasses import dataclass

import yaml

CONFIG_FILE_PATH = "config.yaml"


@dataclass
class Config:
    """
    Config class to manage configuration settings for the application.

    Attributes:
        database_uri (str): URI for the database connection.
        training_data_path (str): Path to the training data file.
        ideal_functions_path (str): Path to the ideal functions file.
        test_data_path (str): Path to the test data file.

    Methods:
        get_instance() -> Config:
            Static method to get the singleton instance of the Config class.
            If the instance does not exist, it reads the configuration from a file
            and creates a new instance.
    """

    database_uri: str
    training_data_path: str
    ideal_functions_path: str
    test_data_path: str

    _instance = None

    @staticmethod
    def get_instance() -> "Config":
        if Config._instance is None:
            with open(CONFIG_FILE_PATH, "r") as file:
                config_dict = yaml.safe_load(file)
            Config._instance = Config(**config_dict)
        return Config._instance
