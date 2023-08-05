from functools import lru_cache

from v3_0.stage.logic.base.check import Check
from v3_0.stage.logic.factories.selector_factory import SelectorFactory


class MetadataCheck(Check):
    @staticmethod
    @lru_cache()
    def instance() -> Check:
        return Check(
            name="metadata check",
            selector=SelectorFactory.instance().metadata(),
        )
