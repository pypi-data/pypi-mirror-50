from v3_0 import TreeBased
from v3_0 import FolderTree


class Category(TreeBased):
    def __init__(self, tree: FolderTree) -> None:
        super().__init__(tree)
