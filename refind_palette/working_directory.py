import os

class WorkingDirectory:
    def __init__(self, root: str, palette_name: str):
        self.root = os.path.abspath(root)
        self.__palette_name = palette_name

        try:
            os.mkdir(self.build())
            os.mkdir(self.build("svg"))

            os.makedirs(self.dist())
            os.mkdir(self.dist("icons"))
            os.mkdir(self.dist("fonts"))
        except FileExistsError:
            pass

        for directory in os.listdir(self.src("svg")):
            try:
                os.mkdir(self.build("svg", directory))
            except FileExistsError:
                pass

    def path(self, *args):
        return os.path.join(self.root, *args)

    def src(self, *args):
        return os.path.join(self.root, "src", *args)

    def build(self, *args):
        return os.path.join(self.root, "build", *args)

    def dist(self, *args):
        return os.path.join(self.root, "dist", self.__palette_name, *args)
