from pathlib import Path
from typing import List

from v3_0 import PathBased
from v3_0 import PathsParser
from v3_0 import Photoset
from v3_0 import Extractor


class StructureExtractor(Extractor):

    def files_to_extract(self, photoset: Photoset) -> List[PathBased]:
        relative_path_strings = self.selector.select(photoset)

        relative_paths = [Path(string) for string in relative_path_strings]

        absolute_paths = [photoset.path / path for path in relative_paths]

        return PathsParser.parse(absolute_paths)
