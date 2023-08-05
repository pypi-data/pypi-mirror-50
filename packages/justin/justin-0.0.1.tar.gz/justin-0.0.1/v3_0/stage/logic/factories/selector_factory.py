from functools import lru_cache

from v3_0 import structure
from v3_0 import Selector
from v3_0 import EditedSelector
from v3_0 import GifSourcesSelector
from v3_0 import MissingGifsSelector
from v3_0 import MetadataSelector
from v3_0 import OddSelectionSelector
from v3_0 import StructureSelector
from v3_0 import UnselectedSelector


class SelectorFactory:
    @staticmethod
    @lru_cache()
    def instance() -> 'SelectorFactory':
        return SelectorFactory()

    @lru_cache()
    def edited(self) -> Selector:
        return EditedSelector()

    @lru_cache()
    def unselected(self) -> Selector:
        return UnselectedSelector()

    @lru_cache()
    def odd_selection(self) -> Selector:
        return OddSelectionSelector()

    @lru_cache()
    def metadata(self) -> Selector:
        return MetadataSelector()

    @lru_cache()
    def missing_gifs(self) -> Selector:
        return MissingGifsSelector()

    @lru_cache()
    def gif_sources(self) -> Selector:
        return GifSourcesSelector()

    @lru_cache()
    def structure(self) -> Selector:
        return StructureSelector(structure.photoset_structure)
