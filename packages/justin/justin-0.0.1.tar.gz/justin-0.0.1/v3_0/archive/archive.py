from typing import Optional

from v3_0.archive.destination import Destination
from v3_0 import TreeBased
from v3_0 import FolderTree


class Archive(TreeBased):
    def __init__(self, tree: FolderTree) -> None:
        super().__init__(tree)

        self.__destinations = [Destination(subtree) for subtree in tree.subtrees]

    def get_destination(self, name: str) -> Optional[Destination]:
        destinations_with_name = [dest for dest in self.__destinations if dest.name == name]

        assert len(destinations_with_name) < 2

        if len(destinations_with_name) == 1:
            return destinations_with_name[0]
        else:
            return None
