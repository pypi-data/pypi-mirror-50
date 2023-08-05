from typing import List

from v3_0 import PartingHelper
from v3_0 import Selector
from v3_0 import Photoset


class MissingGifsSelector(Selector):
    def select(self, photoset: Photoset) -> List[str]:
        parts = PartingHelper.folder_tree_parts(photoset.gif)

        result = []

        for part in parts:
            part_files = set([file.extension.lower().strip(" .") for file in part.files])

            if "gif" not in part_files:
                result.append(part.name)

        return result
