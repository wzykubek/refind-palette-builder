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

    def colorize_svg(self, svg_data: str, color: str):
        return re.sub(r"fill:.*?;", f"fill:{color};", svg_data)

    def process_icon_dir(self, directory: str, color):
        for filename in os.listdir(self.wd.src("svg", directory)):
            with open(self.wd.src("svg", directory, filename), "r") as svg_src_file:
                svg_build_data = self.colorize_svg(svg_src_file.read(), color)
                with open(
                    self.wd.build("svg", directory, filename), "w+"
                ) as svg_build_file:
                    svg_build_file.write(svg_build_data)
                    svg_build_file.close()

    def generate_refind_conf(self):
        config = f"""# Name: {self.palette.name}
# Generated with refind-palette-builder

icons_dir themes/{self.palette.name}/icons
big_icon_size 128
small_icon_size 48
banner themes/{self.palette.name}/icons/bg.png
selection_big themes/{self.palette.name}/icons/selection-big.png
selection_small themes/{self.palette.name}/icons/selection-small.png
# font themes/{self.palette.name}/fonts/{self.palette.font}
"""

        with open(self.wd.dist("theme.conf"), "w+") as refind_conf:
            refind_conf.write(config)
            refind_conf.close()

    def build(self):
        self.process_icon_dir("bg", self.palette.background)
        self.process_icon_dir("sel", self.palette.selection)
        self.process_icon_dir("but", self.palette.button)
        self.process_icon_dir("ind", self.palette.indicator)
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
