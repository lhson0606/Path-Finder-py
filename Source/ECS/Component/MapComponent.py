import esper
import Source.Map.Map as Map


class MapComponent:
    def __init__(self, path):
        self.map = Map.Map(path)

    def clean_up(self):
        self.map.clean_up()
        pass
