import Source.Util.dy as dy


class Map:
    DEFAULT_MAP_DIR = "Resources/Map/"
    DEFAULT_MAP_NAME = "map.txt"

    def __init__(self, path):
        self.path = path
        self.width = 0
        self.height = 0

    def load_or_create(self):
        if not dy.file_exists(self.path):
            self.create()
        else:
            self.load()

    def create(self):
        count = 0

        while dy.file_exists(self.DEFAULT_MAP_DIR + self.DEFAULT_MAP_NAME + str(count)):
            count += 1

        self.path = self.DEFAULT_MAP_DIR + self.DEFAULT_MAP_NAME + str(count)
        self.width = 30
        self.height = 30

        pass

    def load(self):
        pass

    def save(self):
        pass