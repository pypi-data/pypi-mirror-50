from typing import List

from v3_0 import joins
from v3_0 import Selector
from v3_0 import Photoset


class GifSourcesSelector(Selector):
    def select(self, photoset: Photoset) -> List[str]:
        if photoset.gif is None:
            return []

        gif_sources = photoset.gif.flatten()
        sources = photoset.sources

        join = joins.right(
            gif_sources,
            sources,
            lambda gif, source: gif.stem() == source.stem()
        )

        nongifed_sources_names = [source.stem() for gif, source in join if gif is None]

        return nongifed_sources_names
