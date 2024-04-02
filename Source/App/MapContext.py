import glm

import Source.Render.Camera as Camera
import Source.Render.Shader as Shader
import Source.Map.Map as Map


class MapContext:
    def __init__(self, inp_map):
        self.camera = Camera.Camera()
        self.render_processor = None
        self.pick_processor = None
        self.map = inp_map

    def update_projection(self, projection):
        if self.render_processor is not None:
            self.render_processor.update_projection(projection)

    def update_view(self):
        if self.render_processor is not None:
            self.render_processor.update_view(self.camera.view)

    def load_context(self, proj: glm.mat4):
        # update grid view
        self.render_processor.update_grid_view(self.map.width, self.map.height)
        self.update_view()
        self.update_projection(proj)
