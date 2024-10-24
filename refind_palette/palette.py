from configparser import ConfigParser


class Palette:
    def __init__(self, config_path: str):
        config = ConfigParser()
        config.read(config_path)
        self.name = config.get("Theme", "name")
        self.font = config.get("Theme", "font")
        self.background = config.get("Colors", "background")
        self.selection = config.get("Colors", "selection")
        self.button = config.get("Colors", "button")
        self.indicator = config.get("Colors", "indicator")
