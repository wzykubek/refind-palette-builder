#!/usr/bin/env python3

from configparser import ConfigParser
import os
import re
import shutil
from cairosvg import svg2png

class Theme():
    def __init__(self):
        self.src_dir = "src"
        self.build_dir = "build"
        self.dist_dir = "dist"
        self.build()

    def parse_config(self):
        config = ConfigParser()
        config.read("config.ini")
        self.name = config.get("Theme", "name")
        self.font = config.get("Theme", "font")
        self.palette = {
                "bg": config.get("Colors", "background"),
                "sel": config.get("Colors", "selection"),
                "but": config.get("Colors", "buttons"),
                "ind": config.get("Colors", "indicators")
                }

    def prepare_build(self):
        try:
            os.mkdir(self.build_dir)
            os.mkdir(f"{self.build_dir}/svg")
            os.mkdir(self.dist_dir)
            os.mkdir(f"{self.dist_dir}/icons")
        except FileExistsError:
            pass
        for directory in os.listdir(f"{self.src_dir}/svg"):
            try:
                os.mkdir(f"{self.build_dir}/svg/{directory}")
            except FileExistsError:
                pass

    def colorize_svg(self, file_path: str, color: str):
        with open(file_path, "r") as f:
            data = f.read()
            data = re.sub(r'fill:.*?;', f"fill:{color};", data)
            f.close()

            return data

    def process_icons(self, type: str):
        for filename in os.listdir(f"{self.src_dir}/svg/{type}"):
            data = self.colorize_svg(f"{self.src_dir}/svg/{type}/{filename}", self.palette[type])
            with open(f"{self.build_dir}/svg/{type}/{filename}", "w+") as f:
                f.write(data)
                f.close()

    def build(self):
        self.prepare_build()
        self.parse_config()
        self.process_icons("bg")
        self.process_icons("sel")
        self.process_icons("but")
        self.process_icons("ind")
        for filename in os.listdir(f"{self.src_dir}/svg/os"):
            shutil.copy(f"{self.src_dir}/svg/os/{filename}", f"{self.build_dir}/svg/os")

        for directory in os.listdir(f"{self.build_dir}/svg"):
            for filename in os.listdir(f"{self.build_dir}/svg/{directory}"):
                svg2png(url=f"{self.build_dir}/svg/{directory}/{filename}", write_to=f"{self.dist_dir}/icons/{filename.replace('svg', 'png')}")

def main():
    theme = Theme()


if __name__ == "__main__":
    main()
