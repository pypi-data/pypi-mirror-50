from v3_0 import File
from v3_0 import PartingHelper
from v3_0 import GifMaker
from v3_0 import Extractor
from v3_0 import Photoset


class MissingGifsHandler(Extractor):
    def forward(self, photoset: Photoset) -> bool:
        parts = PartingHelper.folder_tree_parts(photoset.gif)

        parts_to_generate = self.selector.select(photoset)

        maker = GifMaker()

        for part_number, part in enumerate(parts, start=1):
            if part.name not in parts_to_generate:
                continue

            print(f"Generating gif for {part.path.relative_to(photoset.path.parent)}")

            if len(parts) == 1:
                name = f"{photoset.name}.gif"
            else:
                name = f"{photoset.name}_{part_number}.gif"

            maker.make_gif(part.path, name)

        return True

    def backwards(self, photoset: Photoset) -> bool:
        parts = PartingHelper.folder_tree_parts(photoset.gif)

        for part in parts:
            for file in part.files:
                if file.extension == ".gifs":
                    File.remove(file.path)

        return True
