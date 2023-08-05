import re
from pathlib import Path
from typing import List

from v3_0.shared import config
from v3_0.shared.helpers.parting_helper import PartingHelper

SETS_KEY = "varied_folders"
PARTS_KEY = "parts"
FILES_KEY = "files"

__SETS = {
    SETS_KEY: {},
}

__PARTS = {
    PARTS_KEY: {},
}

STANDALONE_FILE = "file"

__FILES = {
    FILES_KEY: {},
}

FILES = __FILES

__PARTS_AND_FILES = {
    **__PARTS,
    **__FILES
}


def __categories(names):
    return {name: __SETS for name in names}


__disk_structure = {
    '_meta': STANDALONE_FILE,
    'instagram': __SETS,
    'justin': __categories(config.GROUP_CATEGORIES),
    'photoclub': __SETS,
    'closed': __categories(config.CLOSED_NAMES),
    # 'selections': __SETS,  # only jpegs. should it be sets?
    'unpublished': {
        **{
            "dad": __SETS,
            "mom": __SETS,
        },
        **__SETS,
    },
    'stages': __categories(config.STAGES_NAMES),
    'watermarks': __SETS  # sets?
}

_photoset_structure = {
    'instagram': __FILES,
    'justin': {
        'academ': __PARTS_AND_FILES,
        'artchaos': __PARTS_AND_FILES,
        'countryside': __PARTS_AND_FILES,
        'moments': __PARTS_AND_FILES,
        'nsu': __PARTS_AND_FILES,
        'patterns': __PARTS_AND_FILES,
        'nanoreports': __FILES,
        'reports': FILES,
        'series': __FILES,
        '_meta': __FILES,
        'session': __FILES,
        'piter2017': __PARTS
    },
    'photoclub': __FILES,
    'closed': {name: __FILES for name in config.CLOSED_NAMES},
    'our_people': {name: __FILES for name in config.OUR_PEOPLE_NAMES},
    "gif": __PARTS_AND_FILES,
    "selection": __FILES,
    "preview": __FILES,
    "ondemand": __FILES,
}

_photoset_structure.update(__PARTS_AND_FILES)

__photos_folder = "photos"
METAFILE_NAME = "_meta"


class Structure:
    __FLAG_KEYS = [
        SETS_KEY,
        FILES_KEY,
        PARTS_KEY,
    ]

    __PHOTOSET_NAME_REGEXP = "\d\d\.\d\d\.\d\d\.\w+"

    def __init__(self, name: str, description: dict, path: Path) -> None:
        super().__init__()

        self.__name = name
        self.__substructures = {}
        self.__files = []
        self.__path = path

        for subname, subdesc in description.items():
            if subdesc == STANDALONE_FILE:
                self.__files.append(subname)
            elif subname in Structure.__FLAG_KEYS:
                pass
            else:
                self.__substructures[subname] = Structure(subname, subdesc, self.__path / subname)

        self.__has_implicit_sets = SETS_KEY in description
        self.__has_files = FILES_KEY in description
        self.__has_parts = PARTS_KEY in description

    @property
    def name(self) -> str:
        return self.__name

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def has_substructures(self) -> bool:
        return len(self.substructures) > 0

    @property
    def substructures(self) -> List['Structure']:
        return list(self.__substructures.values())

    @property
    def has_implicit_sets(self) -> bool:
        return self.__has_implicit_sets

    @property
    def has_unlimited_files(self) -> bool:
        return self.__has_files

    @property
    def has_parts(self) -> bool:
        return self.__has_parts

    def __str__(self) -> str:
        return self.__name

    def has_file(self, item: str) -> bool:
        return self.__has_files or item in self.__files

    def has_substructure(self, item: str) -> bool:
        if item in self.__substructures:
            return True
        elif self.has_parts:
            return PartingHelper.is_part_name(item)
        else:
            return False

    def has_set(self, item: str) -> bool:
        return not self.has_substructure(item) and self.has_implicit_sets

    def __getitem__(self, key) -> 'Structure':
        if key in self.__substructures:
            return self.__substructures[key]
        elif self.__has_implicit_sets and re.match(Structure.__PHOTOSET_NAME_REGEXP, key) is not None:
            return Structure(key, _photoset_structure, self.path / key)
        else:
            assert False


disk_structure = Structure("disk", __disk_structure, Path(""))
photoset_structure = Structure("photoset", _photoset_structure, Path(""))
