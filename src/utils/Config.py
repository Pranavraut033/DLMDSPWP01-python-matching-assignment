from dataclasses import dataclass

import yaml

CONFIG_FILE_PATH = "config.yaml"


@dataclass
class Config:
    database_uri: str
    training_data_path: str
    ideal_functions_path: str
    test_data_path: str

    _instance = None

    @staticmethod
    def get_instance() -> "Config":
        """
        Returns the singleton instance of the Config class. If the instance does not exist, reads the configuration from a YAML file and creates it.
        """
        if Config._instance is None:
            with open(CONFIG_FILE_PATH, "r") as file:
                config_dict = yaml.safe_load(file)
            Config._instance = Config(**config_dict)
        return Config._instance
