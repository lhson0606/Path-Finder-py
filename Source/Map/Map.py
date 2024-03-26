import Source.Util.dy as dy

DEFAULT_MAP_DIR = "Resources/Map/"
DEFAULT_MAP_NAME = "map"


def open_existed_map(name):
    if not dy.file_exists(DEFAULT_MAP_DIR + name):
        dy.log.error("Map not found: " + name)
        return None

    with open(DEFAULT_MAP_DIR + name) as file:
        lines = file.readlines()

    map = Map(name)
    map.width = int(lines[0].split(" ")[0])
    map.height = int(lines[0].split(" ")[1])

    for i in range(1, len(lines)):
        line = lines[i].strip()
        for j in range(len(line)):
            pass

    return map


class Map:

    def __init__(self, name, w=25, h=25):
        self.name = name
        self.width = w
        self.height = h
        self.is_dirty = False

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
