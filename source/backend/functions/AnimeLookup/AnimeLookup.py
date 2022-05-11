from source.backend.functions.baseClasses import BaseClass
from source.backend.functions.customTypes import SetMethodDict
from pathlib import Path
import requests

_ANIME_DATABASE_JSON = "https://raw.githubusercontent.com/manami-project/anime-offline-database/master/anime-offline-database-minified.json"


class AnimeLookup(BaseClass):
    def __init__(self):
        super().__init__()
        all_bindings = [
            # ! Work in progress
        ]
        self._create_binding(all_bindings)

        self.__anime_database_path = str(Path(Path(__file__).parent, "anime_database.json"))
        if not Path(self.__anime_database_path).is_file():
            database_text = requests.get(_ANIME_DATABASE_JSON).text
            with open(self.__anime_database_path, "w", encoding="utf-8") as file:
                file.write(database_text)
