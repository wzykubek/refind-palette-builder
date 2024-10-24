from refind_palette.palette import Palette
import os
import shutil
import re
from cairosvg import svg2png


class Generator:
    def __init__(self, palette: Palette):
        self.palette = palette
        self.src_directory = "src"
        self.build_directory = "build"
        self.dist_directory = "dist"

    def prepare_build(self):
        try:
            os.mkdir(self.build_directory)
            os.mkdir(f"{self.build_directory}/svg")
            os.mkdir(self.dist_directory)
            os.mkdir(f"{self.dist_directory}/icons")
        except FileExistsError:
            pass

        for directory in os.listdir(f"{self.src_directory}/svg"):
            try:
                os.mkdir(f"{self.build_directory}/svg/{directory}")
            except FileExistsError:
                pass

    def colorize_svg(self, file_path: str, color: str):
        with open(file_path, "r") as f:
            data = f.read()
            data = re.sub(r"fill:.*?;", f"fill:{color};", data)
            f.close()

            return data

    def process_icons(self, type: str, color):
        for filename in os.listdir(f"{self.src_directory}/svg/{type}"):
            data = self.colorize_svg(
                f"{self.src_directory}/svg/{type}/{filename}", color
            )
            with open(f"{self.build_directory}/svg/{type}/{filename}", "w+") as f:
                f.write(data)
                f.close()

    def generate_refind_conf(self):
        string = f"""# Name: {self.palette.name}
# Generated with refind-palette-builder

icons_dir themes/{self.palette.name}/icons
big_icon_size 128
small_icon_size 48
banner themes/{self.palette.name}/icons/bg.png
selection_big themes/{self.palette.name}/icons/selection-big.png
selection_small themes/{self.palette.name}/icons/selection-small.png
font themes/{self.palette.name}/fonts/{self.palette.font}
"""

        with open(f"{self.dist_directory}/theme.conf", "w+") as f:
            f.write(string)
            f.close()

    def build(self):
        self.prepare_build()
        self.process_icons("bg", self.palette.background)
        self.process_icons("sel", self.palette.background)
        self.process_icons("but", self.palette.background)
        self.process_icons("ind", self.palette.background)
        for filename in os.listdir(f"{self.src_directory}/svg/os"):
            shutil.copy(
                f"{self.src_directory}/svg/os/{filename}",
                f"{self.build_directory}/svg/os",
            )

        for directory in os.listdir(f"{self.build_directory}/svg"):
            for filename in os.listdir(f"{self.build_directory}/svg/{directory}"):
                svg2png(
                    url=f"{self.build_directory}/svg/{directory}/{filename}",
                    write_to=f"{self.dist_directory}/icons/{filename.replace('svg', 'png')}",
                )

        self.generate_refind_conf()
        os.mkdir(f"{self.dist_directory}/fonts")
        # TODO: move fonts to dist directory
