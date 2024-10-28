from refind_palette.palette import Palette
from refind_palette.working_directory import WorkingDirectory
import os
import shutil
import re
from cairosvg import svg2png


class Generator:
    def __init__(self, palette: Palette, working_directory: WorkingDirectory):
        self.palette = palette
        self.wd = working_directory

    def colorize_svg(self, file_path: str, color: str):
        with open(file_path, "r") as f:
            data = f.read()
            data = re.sub(r"fill:.*?;", f"fill:{color};", data)
            f.close()

            return data

    def process_icons(self, directory: str, color):
        for filename in os.listdir(self.wd.src("svg", directory)):
            data = self.colorize_svg(self.wd.src("svg", directory, filename), color)
            with open(self.wd.build("svg", directory, filename), "w+") as f:
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

        with open(self.wd.dist("theme.conf"), "w+") as f:
            f.write(string)
            f.close()

    def build(self):
        self.process_icons("bg", self.palette.background)
        self.process_icons("sel", self.palette.selection)
        self.process_icons("but", self.palette.button)
        self.process_icons("ind", self.palette.indicator)
        for filename in os.listdir(self.wd.src("svg", "os")):
            shutil.copy(
                self.wd.src("svg", "os", filename),
                self.wd.build("svg", "os"),
            )

        for directory in os.listdir(self.wd.build("svg")):
            for filename in os.listdir(self.wd.build("svg", directory)):
                svg2png(
                    url=self.wd.build("svg", directory, filename),
                    write_to=self.wd.dist("icons", filename.replace("svg", "png")),
                )

        self.generate_refind_conf()
