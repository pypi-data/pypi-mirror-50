from pathlib import Path
from typing import List, Optional

from v3_0 import File
from v3_0 import FolderTree


class SingleFolderTree(FolderTree):
    def __init__(self, path: Path) -> None:
        super().__init__(path)

        self.__subtrees = {}
        self.__files = []

        self.refresh()

    @property
    def name(self) -> str:
        return self.path.name

    @property
    def files(self) -> List[File]:
        return self.__files

    @property
    def subtree_names(self) -> List[str]:
        return list(self.__subtrees.keys())

    @property
    def subtrees(self) -> List['FolderTree']:
        return self.__subtree_values

    @property
    def __subtree_values(self) -> List['FolderTree']:
        return list(self.__subtrees.values())

    def __getitem__(self, key: str) -> Optional[FolderTree]:
        return self.__subtrees.get(key)

    def __contains__(self, key: str) -> bool:
        return key in self.subtrees

    def flatten(self) -> List[File]:
        result = self.files.copy()

        for subtree in self.__subtree_values:
            result += subtree.flatten()

        return result

    def refresh(self):
        self.__subtrees = {}
        self.__files = []

        for child in self.path.iterdir():
            if child.is_dir():
                child_tree = SingleFolderTree(child)

                if len(child_tree.flatten()) > 0:
                    self.__subtrees[child.name] = child_tree
                else:
                    child.rmdir()

            elif child.is_file():
                self.files.append(File(child))
            else:
                print("Path not file or dir")

                exit(1)
