import os
from pathlib import Path
from typing import Dict, Iterable, List

from v3_0 import SingleFolderTree
from v3_0 import Disk
from v3_0 import Photoset
from v3_0 import Singleton


class World(Singleton):
    __PHOTOS_FOLDER = "photos"
    __ACTIVE_DISK = "D"

    def __init__(self) -> None:
        super().__init__()

        self.__disks_map = World.__discover_disks()

    @property
    def disks(self) -> Iterable[Disk]:
        return self.__disks_map.values()

    @property
    def active_disk(self) -> Disk:
        return self.__disks_map[World.__ACTIVE_DISK]

    @staticmethod
    def __discover_disks() -> Dict[str, Disk]:
        disks_mapping = {}

        # for disk_letter in string.ascii_uppercase:
        for disk_letter in ["D"]:
            path = Path(disk_letter + ":/") / "photos"

            if os.access(path, os.F_OK) and path.exists():
                disk = Disk(SingleFolderTree(path))

                disks_mapping[disk_letter] = disk

        return disks_mapping

    def __getitem__(self, key) -> List[Photoset]:
        return self.active_disk[key]
