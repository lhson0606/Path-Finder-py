import Source.Render.Camera as Camera
import Source.Render.Shader as Shader
import Source.Map.Map as Map


class MapContext:
    def __init__(self, inp_map):
        self.camera = Camera.Camera()
        self.grid_shader = None
        self.map = inp_map
