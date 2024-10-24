from refind_palette.palette import Palette
import os
import shutil
import re
from cairosvg import svg2png


class Generator:
    def __init__(self, palette: Palette, working_directory: str):
        self.palette = palette
        self.working_directory = working_directory

    def prepare_build(self):
        self.src_directory = os.path.join(self.working_directory, "src")
        self.build_directory = os.path.join(self.working_directory, "build")
        self.dist_directory = os.path.join(
            self.working_directory, "dist", self.palette.name
        )

        try:
            os.mkdir(self.build_directory)
            os.mkdir(os.path.join(self.build_directory, "svg"))

            os.makedirs(self.dist_directory)
            os.mkdir(os.path.join(self.dist_directory, "icons"))
            os.mkdir(os.path.join(self.dist_directory, "fonts"))
        except FileExistsError:
            pass

        for directory in os.listdir(os.path.join(self.src_directory, "svg")):
            try:
                os.mkdir(os.path.join(self.build_directory, "svg", directory))
            except FileExistsError:
                pass

    def colorize_svg(self, file_path: str, color: str):
        with open(file_path, "r") as f:
            data = f.read()
            data = re.sub(r"fill:.*?;", f"fill:{color};", data)
            f.close()

            return data

    def process_icons(self, directory: str, color):
        src_svg_directory = os.path.join(self.src_directory, "svg")
        build_svg_directory = os.path.join(self.build_directory, "svg")
        for filename in os.listdir(os.path.join(src_svg_directory, directory)):
            data = self.colorize_svg(
                os.path.join(src_svg_directory, directory, filename), color
            )
            with open(
                os.path.join(build_svg_directory, directory, filename), "w+"
            ) as f:
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

        with open(os.path.join(self.dist_directory, "theme.conf"), "w+") as f:
            f.write(string)
            f.close()

    def build(self):
        self.prepare_build()
        src_svg_directory = os.path.join(self.src_directory, "svg")
        build_svg_directory = os.path.join(self.build_directory, "svg")
        dist_icons_directory = os.path.join(self.dist_directory, "icons")
        self.process_icons("bg", self.palette.background)
        self.process_icons("sel", self.palette.selection)
        self.process_icons("but", self.palette.button)
        self.process_icons("ind", self.palette.indicator)
        for filename in os.listdir(os.path.join(src_svg_directory, "os")):
            shutil.copy(
                os.path.join(src_svg_directory, "os", filename),
                os.path.join(build_svg_directory, "os"),
            )

        for directory in os.listdir(build_svg_directory):
            for filename in os.listdir(os.path.join(build_svg_directory, directory)):
                svg2png(
                    url=os.path.join(build_svg_directory, directory, filename),
                    write_to=os.path.join(
                        dist_icons_directory, filename.replace("svg", "png")
                    ),
                )

        self.generate_refind_conf()
