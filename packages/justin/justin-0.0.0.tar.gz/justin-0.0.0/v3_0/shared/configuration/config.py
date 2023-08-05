import json
from pathlib import Path


class Config:
    __GROUP_URL_KEY = "group_url"
    __PYVKO_CONFIG_KEY = "pyvko_config"

    def __init__(self, json_object: dict) -> None:
        super().__init__()

        self.__group_url = json_object[Config.__GROUP_URL_KEY]
        self.__pyvko_config = Path(json_object[Config.__PYVKO_CONFIG_KEY])

    @property
    def group_url(self) -> str:
        return self.__group_url

    @property
    def pyvko_config_path(self) -> Path:
        return self.__pyvko_config

    @staticmethod
    def read(path: Path) -> 'Config':
        print(path.absolute())

        with path.open() as config_file:
            config_object = json.load(config_file)

            return Config(config_object)

    def save(self, path: Path):
        json_object = {
            Config.__GROUP_URL_KEY: self.group_url,
            Config.__PYVKO_CONFIG_KEY: str(self.pyvko_config_path)
        }

        with path.open("w") as config_file:
            json.dump(json_object, config_file, indent=4)
