import OpenGL.GL as gl
import esper
from OpenGL.GLU import *

import Source.App.App as App
import Source.ECS.Component.GridComponent as GridComponent
import Source.ECS.Component.RenderComponent as RenderComponent
import Source.Render.Shader as Shader
from Source.Manager.ShaderManager import ShaderType as ShaderType


class RenderProcessor(esper.Processor):
    def __init__(self, app: App):
        # hold a reference to the app to access necessary components
        self.app = app

    def process(self, dt):
        # render all entities with render component
        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader_type = render_data.shader_type

            match shader_type:
                case ShaderType.GRID_SHADER:
                    self.render_as_grid(ent, render_data.shader)
        pass

    def render_as_grid(self, ent, shader: Shader):
        shader.use()
        grid_data = esper.component_for_entity(ent, GridComponent.GridComponent)
        gl.glBindVertexArray(grid_data.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        gl.glBindVertexArray(0)
        shader.stop()
