import argparse
from refind_palette.palette import Palette
from refind_palette.generator import Generator

parser = argparse.ArgumentParser(
    prog="refind-palette",
    description="Tool for generating rEFInd color palette based on regular theme.",
    allow_abbrev=False,
)

parser.add_argument("-c", "--config", default="config.ini")
args = parser.parse_args()

palette = Palette(args.config)
generator = Generator(palette)
generator.build()
