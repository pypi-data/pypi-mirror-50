from functools import lru_cache

from v3_0 import Extractor
from v3_0 import SelectorFactory
from v3_0 import MissingGifsHandler
from v3_0 import MetadataCheck


class ExtractorFactory:
    __EDITED_FOLDER = "edited_sources"
    __ODD_SELECTION_FOLDER = "odd_selection"
    __TO_SELECT_FOLDER = "to_select"
    __UNEXPECTED_STRUCTURES = "unexpected_structures"

    @staticmethod
    @lru_cache()
    def instance() -> 'ExtractorFactory':
        return ExtractorFactory(SelectorFactory.instance())

    def __init__(self, selector_factory: SelectorFactory) -> None:
        super().__init__()
        self.__selector_factory = selector_factory
        self.__metadata_check = MetadataCheck.instance()

    @lru_cache()
    def edited(self) -> Extractor:
        return Extractor(
            selector=self.__selector_factory.edited(),
            filter_folder=ExtractorFactory.__EDITED_FOLDER,
            prechecks=[
                self.__metadata_check
            ]
        )

    @lru_cache()
    def unselected(self) -> Extractor:
        return Extractor(
            selector=self.__selector_factory.unselected(),
            filter_folder=ExtractorFactory.__TO_SELECT_FOLDER,
            prechecks=[
                self.__metadata_check
            ]
        )

    @lru_cache()
    def odd_selection(self) -> Extractor:
        return Extractor(
            selector=self.__selector_factory.odd_selection(),
            filter_folder=ExtractorFactory.__ODD_SELECTION_FOLDER,
            prechecks=[
                self.__metadata_check
            ]
        )

    @lru_cache()
    def missing_gifs(self) -> Extractor:
        return MissingGifsHandler(
            selector=self.__selector_factory.missing_gifs(),
            filter_folder="",
            prechecks=[]
        )

    @lru_cache()
    def structure(self) -> Extractor:
        return Extractor(
            selector=self.__selector_factory.structure(),
            filter_folder=ExtractorFactory.__UNEXPECTED_STRUCTURES,
            prechecks=[
                self.__metadata_check
            ]
        )
