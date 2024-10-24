import argparse
from refind_palette.palette import Palette
from refind_palette.generator import Generator
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
generator = Generator(
    palette=palette, working_directory=os.path.abspath(args.working_directory)
)
generator.build()
