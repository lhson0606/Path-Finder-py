import OpenGL.GL as gl
import esper
from OpenGL.GLU import *

import Source.App.App as App
import Source.ECS.Component.GridComponent as GridComponent
import Source.ECS.Component.ShapeComponent as ShapeComponent
import Source.ECS.Component.RenderComponent as RenderComponent
import Source.Render.Shader as Shader
from Source.Manager.ShaderManager import ShaderType as ShaderType

import glm


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
                case ShaderType.SHAPE_SHADER:
                    self.render_as_shape(ent, render_data.shader)
        pass

    def render_as_grid(self, ent, shader: Shader):
        shader.use()
        grid_data = esper.component_for_entity(ent, GridComponent.GridComponent)
        gl.glBindVertexArray(grid_data.vao)
        gl.glDrawElements(gl.GL_TRIANGLES, 6, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        gl.glBindVertexArray(0)
        shader.stop()
        pass

    def render_as_shape(self, ent, shader):
        shader.use()
        shape_data = esper.component_for_entity(ent, ShapeComponent.ShapeComponent)
        gl.glBindVertexArray(shape_data.vao)
        # gl.glDrawArrays(gl.GL_TRIANGLES, 0, shape_data.vertex_count)
        gl.glDrawElements(gl.GL_TRIANGLES, shape_data.vertex_count, gl.GL_UNSIGNED_INT, ctypes.c_void_p(0))
        gl.glBindVertexArray(0)
        shader.stop()
        pass

    def update_projection(self, projection: glm.mat4):
        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader = render_data.shader
            shader.use()
            shader.set_mat4("projection", projection)
            shader.stop()
        pass

    def update_view(self, view: glm.mat4):
        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader = render_data.shader
            shader.use()
            shader.set_mat4("view", view)
            shader.stop()
        pass

    def update_grid_view(self, width, height):
        for ent, (render_data) in esper.get_component(RenderComponent.RenderComponent):
            shader_type = render_data.shader_type

            if shader_type == ShaderType.GRID_SHADER:
                shader = render_data.shader
                shader.use()
                shader.set_float("gridWidth", width)
                shader.set_float("gridHeight", height)
                shader.stop()
        pass

