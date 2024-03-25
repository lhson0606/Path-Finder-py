import Source.Util.dy as dy

DEFAULT_MAP_DIR = "Resources/Map/"
DEFAULT_MAP_NAME = "map"


class Map:

    def __init__(self, path):
        self.path = path
        self.width = 0
        self.height = 0
        self.is_dirty = False

    def load_or_create(self):
        if not dy.file_exists(self.path):
            self.create()
        else:
            self.load()

    def create(self):
        count = 0

        pass

    def load(self):
        pass

    def save(self):
        pass

    @staticmethod
    def get_new_map_name(directory=DEFAULT_MAP_DIR):
        count = 0

        while dy.file_exists(directory + DEFAULT_MAP_NAME + str(count) + ".txt"):
            count += 1

        return DEFAULT_MAP_NAME + str(count) + ".txt"

    @staticmethod
    def is_map_name_existed(name, directory=DEFAULT_MAP_DIR):
        return dy.file_exists(directory + name)
