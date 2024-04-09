import Source.Map.Map as Map
import glm


class VisualizedAlgorithm:
    def __init__(self, m: Map):
        self.map = m
        self.vao = -1
        self.vbo_pos = -1
        self.ebo = -1
        self.path_entities = []

