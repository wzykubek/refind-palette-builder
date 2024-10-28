import argparse
from .palette import Palette
from .generator import Generator
from .working_directory import WorkingDirectory
import os

parser = argparse.ArgumentParser(
    prog="refind-palette",
    description="Tool for generating rEFInd color palette based on regular theme.",
    allow_abbrev=False,
)

parser.add_argument("-c", "--config", default="config.ini")
parser.add_argument("-w", "--working-directory", default=os.getcwd())
args = parser.parse_args()

palette = Palette(args.config)
wd = WorkingDirectory(root=args.working_directory, palette_name=palette.name)
generator = Generator(
    palette=palette, working_directory=wd
)
generator.build()
